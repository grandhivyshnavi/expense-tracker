import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from email_utils import send_email_alert

load_dotenv()
Base = declarative_base()
engine = create_engine("sqlite:///expenses.db")
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    budgets = relationship("Budget", backref="user")
    expenses = relationship("Expense", backref="user")

class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String)
    amount = Column(Float)
    month = Column(String)  # e.g., "2024-04"

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String)
    amount = Column(Float)
    date = Column(Date)

Base.metadata.create_all(engine)

def add_user(name, email):
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    print(f"User {name} added.")

def set_budget(user_name, category, amount, month):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return
    budget = Budget(user_id=user.id, category=category, amount=amount, month=month)
    session.add(budget)
    session.commit()
    print(f"Budget set: ₹{amount} for {category} in {month}.")

def log_expense(user_name, category, amount):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return
    today = datetime.now().date()
    expense = Expense(user_id=user.id, category=category, amount=amount, date=today)
    session.add(expense)
    session.commit()
    print(f"Logged ₹{amount} spent on {category}.")

    # Budget check and alerts
    month = datetime.now().strftime("%Y-%m")
    budget = session.query(Budget).filter_by(user_id=user.id, category=category, month=month).first()
    if budget:
        total_spent = sum(e.amount for e in user.expenses if e.category == category and e.date.strftime("%Y-%m") == month)
        if total_spent > budget.amount:
            print(f"⚠️ Budget exceeded for {category}!")
            send_email_alert(user.email, f"You have exceeded your budget for {category} in {month}.")
        elif total_spent > 0.9 * budget.amount:
            print(f"⚠️ Alert: 90% of budget used for {category}.")
            send_email_alert(user.email, f"You're about to exceed your budget for {category} in {month}.")

def show_report(user_name, month):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    print(f"\n📊 Report for {user.name} - {month}")
    categories = session.query(Budget).filter_by(user_id=user.id, month=month).all()
    for budget in categories:
        spent = sum(e.amount for e in user.expenses if e.category == budget.category and e.date.strftime("%Y-%m") == month)
        print(f"Category: {budget.category} | Spent: ₹{spent:.2f} / Budget: ₹{budget.amount:.2f}")

# Example interaction
if __name__ == "__main__":
    while True:
        print("\n1. Add User\n2. Set Budget\n3. Log Expense\n4. Show Report\n5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            name = input("Enter name: ")
            email = input("Enter email: ")
            add_user(name, email)
        elif choice == "2":
            name = input("Enter user name: ")
            category = input("Category (e.g., Food): ")
            amount = float(input("Budget amount: "))
            month = input("Month (YYYY-MM): ")
            set_budget(name, category, amount, month)
        elif choice == "3":
            name = input("Enter user name: ")
            category = input("Category: ")
            amount = float(input("Amount spent: "))
            log_expense(name, category, amount)
        elif choice == "4":
            name = input("Enter user name: ")
            month = input("Month (YYYY-MM): ")
            show_report(name, month)
        elif choice == "5":
            break
        else:
            print("Invalid option.")
