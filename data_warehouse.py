import json
import datetime
import hashlib
import random

class CloudDatabase:
    def __init__(self, db_name, db_type="Relational"):
        self.db_name = db_name
        self.db_type = db_type
        self.tables = {}
        self.connection_string = f"cloud://{db_name}.database.com:5432"
        self.status = "Available"
        self.created_at = datetime.datetime.now().isoformat()
        self.backups = []

        print(f"✅ Database '{db_name}' provisioned successfully!")
        print(f"   Type: {db_type}")
        print(f"   Connection String: {self.connection_string}")

    def create_table(self, table_name, columns):
        if table_name in self.tables:
            print(f"⚠️ Table '{table_name}' already exists!")
            return False

        self.tables[table_name] = {
            "columns": columns,
            "records": [],
            "created_at": datetime.datetime.now().isoformat(),
            "row_count": 0
        }

        print(f"✅ Table '{table_name}' created successfully!")
        print(f"   Columns: {', '.join(columns)}")
        return True

    def insert_record(self, table_name, record):
        if table_name not in self.tables:
            print(f"❌ Table '{table_name}' not found!")
            return False

        record_id = f"REC-{random.randint(10000, 99999)}"
        record_data = {
            "id": record_id,
            "data": record,
            "created_at": datetime.datetime.now().isoformat()
        }

        self.tables[table_name]["records"].append(record_data)
        self.tables[table_name]["row_count"] += 1

        print(f"✅ Record inserted into '{table_name}'")
        print(f"   ID: {record_id}")
        return True

    def get_all_records(self, table_name):
        if table_name not in self.tables:
            print(f"❌ Table '{table_name}' not found!")
            return []

        return self.tables[table_name]["records"]

    def get_record_by_id(self, table_name, record_id):
        if table_name not in self.tables:
            print(f"❌ Table '{table_name}' not found!")
            return None

        for record in self.tables[table_name]["records"]:
            if record["id"] == record_id:
                return record

        return None

    def delete_record(self, table_name, record_id):
        if table_name not in self.tables:
            print(f"❌ Table '{table_name}' not found!")
            return False

        for i, record in enumerate(self.tables[table_name]["records"]):
            if record["id"] == record_id:
                del self.tables[table_name]["records"][i]
                self.tables[table_name]["row_count"] -= 1
                print(f"✅ Record '{record_id}' deleted!")
                return True

        print(f"❌ Record '{record_id}' not found!")
        return False

    def create_backup(self):
        backup = {
            "backup_id": f"BACKUP-{random.randint(1000, 9999)}",
            "timestamp": datetime.datetime.now().isoformat(),
            "tables": {}
        }

        for table_name, table_data in self.tables.items():
            backup["tables"][table_name] = {
                "columns": table_data["columns"],
                "records": table_data["records"],
                "row_count": table_data["row_count"]
            }

        self.backups.append(backup)
        print(f"✅ Backup '{backup['backup_id']}' created successfully!")
        return backup

    def display_summary(self):
        print("\n" + "=" * 60)
        print(f"   DATABASE SUMMARY: {self.db_name}")
        print("=" * 60)
        print(f"Type: {self.db_type}")
        print(f"Status: {self.status}")
        print(f"Created: {self.created_at}")
        print(f"Tables: {len(self.tables)}")

        for table_name, table_data in self.tables.items():
            print(f"\n  📋 Table: {table_name}")
            print(f"     Row Count: {table_data['row_count']}")
            print(f"     Columns: {', '.join(table_data['columns'])}")

            if table_data['row_count'] > 0:
                print("     Sample Records:")
                for i, record in enumerate(table_data['records'][:3], 1):
                    print(f"       {i}. {record['data']}")

        print("=" * 60)

class DataWarehouseSimulator:
    def __init__(self):
        self.database = None

    def run(self):
        print("\n" + "=" * 60)
        print("   THE DATA WAREHOUSE - CLOUD COMPUTING")
        print("=" * 60)

        print("\n[1] Provisioning Cloud Database...")
        self.database = CloudDatabase("decodelabs-db", "Relational (PostgreSQL)")

        print("\n[2] Creating 'Interns' Table...")
        columns = ["Name", "Role", "Email", "Phone", "Department", "JoiningDate"]
        self.database.create_table("Interns", columns)

        print("\n[3] Inserting Dummy Records...")
        dummy_data = [
            ("Aiman Zahoor", "AI Engineer", "aimanzahoor87@gmail.com", "0313-7661020", "Artificial Intelligence", "2026-06-01"),
            ("Ali Hassan", "Backend Developer", "ali@decodelabs.com", "0300-1234567", "Backend", "2026-06-15"),
            ("Sara Ahmed", "Frontend Developer", "sara@decodelabs.com", "0301-7654321", "Frontend", "2026-07-01"),
            ("Usman Malik", "Cloud Engineer", "usman@decodelabs.com", "0302-9876543", "Cloud", "2026-07-15"),
            ("Fatima Khan", "Data Scientist", "fatima@decodelabs.com", "0303-4567890", "Data Science", "2026-08-01")
        ]

        for name, role, email, phone, dept, date in dummy_data:
            record = {
                "Name": name,
                "Role": role,
                "Email": email,
                "Phone": phone,
                "Department": dept,
                "JoiningDate": date
            }
            self.database.insert_record("Interns", record)

        print("\n[4] Displaying All Records...")
        records = self.database.get_all_records("Interns")
        print("\nAll Interns:")
        print("-" * 60)
        for record in records:
            data = record["data"]
            print(f"ID: {record['id']}")
            print(f"  Name: {data['Name']}")
            print(f"  Role: {data['Role']}")
            print(f"  Email: {data['Email']}")
            print(f"  Phone: {data['Phone']}")
            print(f"  Department: {data['Department']}")
            print(f"  Joining Date: {data['JoiningDate']}")
            print("-" * 60)

        print("\n[5] Creating Database Backup...")
        self.database.create_backup()

        print("\n[6] Database Summary:")
        self.database.display_summary()

        print("\n[7] Simulating Python Connection Test...")
        print(f"✅ Connected to {self.database.db_name}")
        print(f"   Connection String: {self.database.connection_string}")
        print(f"   Tables Found: {len(self.database.tables)}")
        print(f"   Total Records: {sum(t['row_count'] for t in self.database.tables.values())}")

        print("\n" + "=" * 60)
        print("   DATA WAREHOUSE COMPLETE")
        print("=" * 60)

def main():
    simulator = DataWarehouseSimulator()
    simulator.run()

if __name__ == "__main__":
    main()