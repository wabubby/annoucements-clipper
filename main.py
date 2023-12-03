import clipper

def main():
    # PUT YOUR SOURCE FOLDER HERE!
    source_dir = r"C:\Personal\youtube download\Announcements Songs"

    # PUT YOUR DESTINATION FOLDER HERE!
    export_dir = r"C:\Personal\youtube download\Announcements Export"

    clipper.clip(source_dir, export_dir)

if __name__ == "__main__":
    main()