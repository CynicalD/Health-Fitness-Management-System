import psycopg2


# --- Database connection helper --- #

def get_connection():
    """
    Open a new connection to the gym_management database.
    Assumes the current OS user has access (same as when you ran psql).
    """
    return psycopg2.connect(dbname="gym_management")


# --- Member operations --- #

def register_member():
    print("\n--- Register New Member ---")
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone (optional): ").strip()
    goal_description = input("Fitness goal (optional): ").strip()

    if not first_name or not last_name or not email:
        print("First name, last name, and email are required.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO member (first_name, last_name, email, phone, goal_description)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING member_id;
                    """,
                    (first_name, last_name, email, phone or None, goal_description or None),
                )
                member_id = cur.fetchone()[0]
                conn.commit()
                print(f"\nMember registered successfully with member_id = {member_id}\n")
    except psycopg2.errors.UniqueViolation:
        print("\nError: A member with that email already exists.\n")
    except Exception as e:
        print(f"\nUnexpected error while registering member: {e}\n")


def list_members():
    """
    Helper to see data from DB (for debugging).
    """
    print("\n--- Current Members ---")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT member_id, first_name, last_name, email
                    FROM member
                    ORDER BY member_id;
                    """
                )
                rows = cur.fetchall()
                if not rows:
                    print("No members found.\n")
                    return
                for member_id, first_name, last_name, email in rows:
                    print(f"{member_id}: {first_name} {last_name} <{email}>")
                print()
    except Exception as e:
        print(f"\nUnexpected error while listing members: {e}\n")

def update_member_profile():
    print("\n--- Update Member Profile ---")
    email = input("Enter the member's email: ").strip()

    if not email:
        print("Email is required to find the member.\n")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Find the member by email
                cur.execute(
                    """
                    SELECT member_id, first_name, last_name, phone, goal_description
                    FROM member
                    WHERE email = %s;
                    """,
                    (email,)
                )
                row = cur.fetchone()

                if not row:
                    print("\nNo member found with that email.\n")
                    return

                member_id, first_name, last_name, phone, goal_description = row

                print(f"\nCurrent info for {first_name} {last_name}:")
                print(f"Phone: {phone}")
                print(f"Goal:  {goal_description}\n")

                print("Press Enter to keep the existing value.\n")

                new_first_name = input(f"New first name [{first_name}]: ").strip()
                new_last_name = input(f"New last name [{last_name}]: ").strip()
                new_phone = input(f"New phone [{phone}]: ").strip()
                new_goal = input(f"New goal [{goal_description}]: ").strip()

                # If user leaves a field blank, keep the old value
                updated_first_name = new_first_name or first_name
                updated_last_name = new_last_name or last_name
                updated_phone = new_phone or phone
                updated_goal = new_goal or goal_description

                cur.execute(
                    """
                    UPDATE member
                    SET first_name = %s,
                        last_name = %s,
                        phone = %s,
                        goal_description = %s
                    WHERE member_id = %s;
                    """,
                    (updated_first_name, updated_last_name, updated_phone, updated_goal, member_id)
                )
                conn.commit()
                print("\nMember profile updated successfully.\n")

    except Exception as e:
        print(f"\nUnexpected error while updating member profile: {e}\n")

def add_health_metric():
    print("\n--- Add Health Metric ---")
    email = input("Enter the member's email: ").strip()

    if not email:
        print("Email is required to find the member.\n")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Find the member by email
                cur.execute(
                    """
                    SELECT member_id, first_name, last_name
                    FROM member
                    WHERE email = %s;
                    """,
                    (email,)
                )
                row = cur.fetchone()

                if not row:
                    print("\nNo member found with that email.\n")
                    return

                member_id, first_name, last_name = row

                print(f"\nAdding health metric for {first_name} {last_name} ({email})")
                print("Leave a field blank if you don't want to record it.\n")

                weight_input = input("Weight (kg): ").strip()
                hr_input = input("Resting heart rate (bpm): ").strip()

                weight_kg = float(weight_input) if weight_input else None
                resting_hr = int(hr_input) if hr_input else None

                cur.execute(
                    """
                    INSERT INTO health_metric (member_id, weight_kg, resting_heart_rate)
                    VALUES (%s, %s, %s);
                    """,
                    (member_id, weight_kg, resting_hr)
                )
                conn.commit()
                print("\nHealth metric recorded successfully.\n")

    except ValueError:
        print("\nInvalid numeric input. Please enter valid numbers for weight and heart rate.\n")
    except Exception as e:
        print(f"\nUnexpected error while adding health metric: {e}\n")

# --- Menus --- #
def member_menu():
    while True:
        print("=== Member Menu ===")
        print("1) Register new member")
        print("2) List members (debug/testing)")
        print("3) Update member profile")
        print("4) Add health metric")
        print("0) Back to main menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_member()
        elif choice == "2":
            list_members()
        elif choice == "3":
            update_member_profile()
        elif choice == "4":
            add_health_metric()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.\n")

def trainer_menu():
    print("\nTrainer menu is not implemented yet.\n")


def admin_menu():
    print("\nAdmin menu is not implemented yet.\n")


def main():
    while True:
        print("=== Gym Management System ===")
        print("1) Member")
        print("2) Trainer")
        print("3) Admin")
        print("0) Exit")
        choice = input("Choose your role: ").strip()

        if choice == "1":
            member_menu()
        elif choice == "2":
            trainer_menu()
        elif choice == "3":
            admin_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
