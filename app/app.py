import psycopg2


#connecting to db

def get_connection():

    #Open a new connection to the gym_management database.
   
    return psycopg2.connect(dbname="gym_management")


# --- Member opps --- #

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

    #Helper to see data from DB 
    
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

def register_for_class():
    print("\n--- Group Class Registration ---")
    email = input("Enter the member's email: ").strip()

    if not email:
        print("Email is required to find the member.\n")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # 1) Find the member by email
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
                print(f"\nRegistering {first_name} {last_name} ({email}) for a class.\n")

                # 2) Show available classes with current count vs capacity
                cur.execute(
                    """
                    SELECT fc.class_id,
                           fc.class_name,
                           fc.start_time,
                           fc.capacity,
                           COUNT(cr.member_id) AS current_count
                    FROM fitness_class fc
                    LEFT JOIN class_registration cr
                      ON fc.class_id = cr.class_id
                    GROUP BY fc.class_id, fc.class_name, fc.start_time, fc.capacity
                    ORDER BY fc.start_time;
                    """
                )
                classes = cur.fetchall()

                if not classes:
                    print("No classes are scheduled.\n")
                    return

                print("Available classes:")
                for class_id, class_name, start_time, capacity, current_count in classes:
                    spots_left = capacity - current_count
                    print(
                        f"  ID {class_id}: {class_name} at {start_time} "
                        f"(capacity {capacity}, enrolled {current_count}, spots left {spots_left})"
                    )

                print()
                class_input = input("Enter class ID to register (or press Enter to cancel): ").strip()
                if not class_input:
                    print("Registration cancelled.\n")
                    return

                try:
                    class_id = int(class_input)
                except ValueError:
                    print("Invalid class ID.\n")
                    return

                # 3) Check that the class exists and get capacity
                cur.execute(
                    """
                    SELECT capacity
                    FROM fitness_class
                    WHERE class_id = %s;
                    """,
                    (class_id,)
                )
                row = cur.fetchone()
                if not row:
                    print("No class found with that ID.\n")
                    return

                class_capacity = row[0]

                # 4) Check if member already registered
                cur.execute(
                    """
                    SELECT 1
                    FROM class_registration
                    WHERE member_id = %s AND class_id = %s;
                    """,
                    (member_id, class_id)
                )
                if cur.fetchone():
                    print("\nMember is already registered in this class.\n")
                    return

                # 5) Check current enrollment vs capacity
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM class_registration
                    WHERE class_id = %s;
                    """,
                    (class_id,)
                )
                current_count = cur.fetchone()[0]

                if current_count >= class_capacity:
                    print("\nCannot register: class is already full.\n")
                    return

                # 6) Insert registration
                cur.execute(
                    """
                    INSERT INTO class_registration (member_id, class_id)
                    VALUES (%s, %s);
                    """,
                    (member_id, class_id)
                )
                conn.commit()
                print("\nSuccessfully registered for the class.\n")

    except Exception as e:
        print(f"\nUnexpected error while registering for class: {e}\n")

# --- Menus --- #
def member_menu():
    while True:
        print("=== Member Menu ===")
        print("1) Register new member")
        print("2) List members")
        print("3) Update member profile")
        print("4) Add health metric")
        print("5) Register for group class")
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
        elif choice == "5":
            register_for_class()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.\n")

def trainer_view_schedule():
    print("\n--- Trainer Schedule View ---")
    email = input("Enter trainer's email: ").strip()

    if not email:
        print("Email is required to find the trainer.\n")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # 1) Find trainer by email
                cur.execute(
                    """
                    SELECT trainer_id, first_name, last_name
                    FROM trainer
                    WHERE email = %s;
                    """,
                    (email,)
                )
                row = cur.fetchone()

                if not row:
                    print("\nNo trainer found with that email.\n")
                    return

                trainer_id, first_name, last_name = row
                print(f"\nSchedule for {first_name} {last_name} ({email}):\n")

                # 2) Get all classes for this trainer with enrolled count
                cur.execute(
                    """
                    SELECT fc.class_id,
                           fc.class_name,
                           fc.start_time,
                           fc.end_time,
                           r.room_id,
                           r.capacity AS room_capacity,
                           COUNT(cr.member_id) AS enrolled_count
                    FROM fitness_class fc
                    JOIN room r ON fc.room_id = r.room_id
                    LEFT JOIN class_registration cr
                      ON fc.class_id = cr.class_id
                    WHERE fc.trainer_id = %s
                    GROUP BY fc.class_id, fc.class_name, fc.start_time, fc.end_time, r.room_id, r.capacity
                    ORDER BY fc.start_time;
                    """,
                    (trainer_id,)
                )
                classes = cur.fetchall()

                if not classes:
                    print("This trainer has no scheduled classes.\n")
                    return

                for class_id, class_name, start_time, end_time, room_id, room_capacity, enrolled_count in classes:
                    print(
                        f"Class ID {class_id}: {class_name}\n"
                        f"  Time: {start_time} -> {end_time}\n"
                        f"  Room: {room_id} (capacity {room_capacity})\n"
                        f"  Enrolled: {enrolled_count}\n"
                    )

    except Exception as e:
        print(f"\nUnexpected error while viewing trainer schedule: {e}\n")

def trainer_view_class_members():
    print("\n--- View Members in My Class ---")
    email = input("Enter trainer's email: ").strip()

    if not email:
        print("Email is required to find the trainer.\n")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # 1) Find trainer by email
                cur.execute(
                    """
                    SELECT trainer_id, first_name, last_name
                    FROM trainer
                    WHERE email = %s;
                    """,
                    (email,)
                )
                row = cur.fetchone()

                if not row:
                    print("\nNo trainer found with that email.\n")
                    return

                trainer_id, first_name, last_name = row
                print(f"\nClasses for {first_name} {last_name} ({email}):\n")

                # 2) List only classes taught by this trainer
                cur.execute(
                    """
                    SELECT fc.class_id,
                           fc.class_name,
                           fc.start_time,
                           fc.end_time
                    FROM fitness_class fc
                    WHERE fc.trainer_id = %s
                    ORDER BY fc.start_time;
                    """,
                    (trainer_id,)
                )
                classes = cur.fetchall()

                if not classes:
                    print("This trainer has no scheduled classes.\n")
                    return

                for class_id, class_name, start_time, end_time in classes:
                    print(
                        f"  ID {class_id}: {class_name} "
                        f"({start_time} -> {end_time})"
                    )

                print()
                class_input = input("Enter class ID to view members (or press Enter to cancel): ").strip()
                if not class_input:
                    print("Cancelled.\n")
                    return

                try:
                    class_id = int(class_input)
                except ValueError:
                    print("Invalid class ID.\n")
                    return

                # 3) Ensure the chosen class actually belongs to this trainer
                cur.execute(
                    """
                    SELECT 1
                    FROM fitness_class
                    WHERE class_id = %s AND trainer_id = %s;
                    """,
                    (class_id, trainer_id)
                )
                if not cur.fetchone():
                    print("\nThat class is not taught by this trainer.\n")
                    return

                # 4) Get members registered in this class, with latest health metric if available
                cur.execute(
                    """
                    SELECT m.member_id,
                           m.first_name,
                           m.last_name,
                           m.email,
                           m.goal_description,
                           hm.weight_kg,
                           hm.resting_heart_rate,
                           hm.recorded_at
                    FROM class_registration cr
                    JOIN member m
                      ON cr.member_id = m.member_id
                    LEFT JOIN (
                        SELECT DISTINCT ON (member_id)
                               member_id,
                               weight_kg,
                               resting_heart_rate,
                               recorded_at
                        FROM health_metric
                        ORDER BY member_id, recorded_at DESC
                    ) hm
                      ON hm.member_id = m.member_id
                    WHERE cr.class_id = %s
                    ORDER BY m.last_name, m.first_name;
                    """,
                    (class_id,)
                )
                members = cur.fetchall()

                if not members:
                    print("\nNo members are registered for this class.\n")
                    return

                print("\nMembers in this class:\n")
                for (
                    member_id,
                    m_first,
                    m_last,
                    m_email,
                    goal_description,
                    weight_kg,
                    resting_hr,
                    recorded_at,
                ) in members:
                    goal_text = goal_description or "N/A"
                    if recorded_at is not None:
                        metric_text = f"{weight_kg} kg, {resting_hr} bpm (as of {recorded_at})"
                    else:
                        metric_text = "No health metrics recorded"
                    print(
                        f"- {m_first} {m_last} <{m_email}> (Member ID {member_id})\n"
                        f"  Goal: {goal_text}\n"
                        f"  Latest metric: {metric_text}\n"
                    )

    except Exception as e:
        print(f"\nUnexpected error while viewing class members: {e}\n")

def trainer_menu():
    while True:
        print("\n=== Trainer Menu ===")
        print("1) View my class schedule")
        print("2) View members in one of my classes")
        print("0) Back to main menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            trainer_view_schedule()
        elif choice == "2":
            trainer_view_class_members()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.\n")

def admin_create_class():
    print("\n--- Admin: Create New Fitness Class ---")
    class_name = input("Class name: ").strip()

    if not class_name:
        print("Class name is required.\n")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # 1) Show trainers so admin can pick one
                cur.execute(
                    """
                    SELECT trainer_id, first_name, last_name
                    FROM trainer
                    ORDER BY trainer_id;
                    """
                )
                trainers = cur.fetchall()
                if not trainers:
                    print("No trainers exist. Cannot create a class.\n")
                    return

                print("\nAvailable trainers:")
                for trainer_id, first_name, last_name in trainers:
                    print(f"  {trainer_id}: {first_name} {last_name}")

                trainer_input = input("Choose trainer_id: ").strip()
                try:
                    trainer_id = int(trainer_input)
                except ValueError:
                    print("Invalid trainer_id.\n")
                    return

                cur.execute(
                    "SELECT 1 FROM trainer WHERE trainer_id = %s;",
                    (trainer_id,)
                )
                if not cur.fetchone():
                    print("No trainer found with that ID.\n")
                    return

                # 2) Show rooms so admin can pick one
                cur.execute(
                    """
                    SELECT room_id, capacity
                    FROM room
                    ORDER BY room_id;
                    """
                )
                rooms = cur.fetchall()
                if not rooms:
                    print("No rooms exist. Cannot create a class.\n")
                    return

                print("\nAvailable rooms:")
                for room_id, room_capacity in rooms:
                    print(f"  {room_id}: capacity {room_capacity}")

                room_input = input("Choose room_id: ").strip()
                try:
                    room_id = int(room_input)
                except ValueError:
                    print("Invalid room_id.\n")
                    return

                cur.execute(
                    "SELECT 1 FROM room WHERE room_id = %s;",
                    (room_id,)
                )
                if not cur.fetchone():
                    print("No room found with that ID.\n")
                    return

                # 3) Get times and capacity
                print("\nEnter times in format YYYY-MM-DD HH:MM (24-hour clock).")
                start_time = input("Start time: ").strip()
                end_time = input("End time:   ").strip()

                capacity_input = input("Class capacity (max participants): ").strip()
                try:
                    capacity = int(capacity_input)
                except ValueError:
                    print("Invalid capacity.\n")
                    return

                if capacity <= 0:
                    print("Capacity must be a positive integer.\n")
                    return

                # 4) Insert the new class
                cur.execute(
                    """
                    INSERT INTO fitness_class (class_name, trainer_id, room_id, start_time, end_time, capacity)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING class_id;
                    """,
                    (class_name, trainer_id, room_id, start_time, end_time, capacity)
                )
                class_id = cur.fetchone()[0]
                conn.commit()
                print(f"\nCreated class '{class_name}' with class_id = {class_id}.\n")

    except Exception as e:
        print(f"\nUnexpected error while creating class: {e}\n")

def admin_update_class():
    print("\n--- Admin: Update Existing Fitness Class ---")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # 1) List existing classes
                cur.execute(
                    """
                    SELECT fc.class_id,
                           fc.class_name,
                           fc.start_time,
                           fc.end_time,
                           fc.capacity,
                           t.first_name,
                           t.last_name,
                           r.room_id
                    FROM fitness_class fc
                    JOIN trainer t ON fc.trainer_id = t.trainer_id
                    JOIN room r ON fc.room_id = r.room_id
                    ORDER BY fc.class_id;
                    """
                )
                classes = cur.fetchall()

                if not classes:
                    print("No classes exist to update.\n")
                    return

                print("Existing classes:")
                for (
                    class_id,
                    class_name,
                    start_time,
                    end_time,
                    capacity,
                    t_first,
                    t_last,
                    room_id,
                ) in classes:
                    print(
                        f"  ID {class_id}: {class_name} "
                        f"({start_time} -> {end_time}), "
                        f"room {room_id}, trainer {t_first} {t_last}, "
                        f"capacity {capacity}"
                    )

                class_input = input("\nEnter class ID to update (or press Enter to cancel): ").strip()
                if not class_input:
                    print("Update cancelled.\n")
                    return

                try:
                    class_id = int(class_input)
                except ValueError:
                    print("Invalid class ID.\n")
                    return

                # 2) Fetch current values for selected class
                cur.execute(
                    """
                    SELECT class_name, start_time, end_time, capacity
                    FROM fitness_class
                    WHERE class_id = %s;
                    """,
                    (class_id,)
                )
                row = cur.fetchone()
                if not row:
                    print("No class found with that ID.\n")
                    return

                class_name, current_start, current_end, current_capacity = row

                print(f"\nUpdating class ID {class_id}: {class_name}")
                print(f"Current start time: {current_start}")
                print(f"Current end time:   {current_end}")
                print(f"Current capacity:   {current_capacity}\n")
                print("Press Enter to keep the existing value.\n")

                new_start = input(f"New start time [{current_start}]: ").strip()
                new_end = input(f"New end time   [{current_end}]: ").strip()
                new_capacity_input = input(f"New capacity   [{current_capacity}]: ").strip()

                # 3) Decide final values
                updated_start = new_start or current_start
                updated_end = new_end or current_end

                if new_capacity_input:
                    try:
                        updated_capacity = int(new_capacity_input)
                    except ValueError:
                        print("Invalid capacity. Must be an integer.\n")
                        return
                    if updated_capacity <= 0:
                        print("Capacity must be a positive integer.\n")
                        return
                else:
                    updated_capacity = current_capacity

                # 4) Apply update
                cur.execute(
                    """
                    UPDATE fitness_class
                    SET start_time = %s,
                        end_time = %s,
                        capacity = %s
                    WHERE class_id = %s;
                    """,
                    (updated_start, updated_end, updated_capacity, class_id)
                )
                conn.commit()
                print("\nClass updated successfully.\n")

    except Exception as e:
        print(f"\nUnexpected error while updating class: {e}\n")

def admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        print("1) Create new fitness class")
        print("2) Update existing fitness class")
        print("0) Back to main menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            admin_create_class()
        elif choice == "2":
            admin_update_class()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.\n")


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
