import os
import PyPDF2
import pandas as pd


def split_pdf(input_pdf_path, output_dir, names_list):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the PDF file
    with open(input_pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Print number of pages in the PDF for debugging
        num_pages = len(pdf_reader.pages)
        print(f"Number of pages in PDF: {num_pages}")

        # Check if the number of pages matches the number of names
        if num_pages != len(names_list):
            raise ValueError(f"The number of pages in the PDF ({num_pages}) does not match the number of names provided ({len(names_list)}).")

        # Iterate through all the pages and save each as a separate PDF
        for i, page in enumerate(pdf_reader.pages):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(page)

            # Define the output file path
            output_pdf_path = os.path.join(output_dir, f"{names_list[i]}.pdf")

            # Write the single page to a new PDF file
            with open(output_pdf_path, 'wb') as output_pdf_file:
                pdf_writer.write(output_pdf_file)

            print(f"Page {i + 1} saved as {output_pdf_path}")


def main():
    # Define paths
    input_pdf_path = r'C:\Users\dhany\Downloads\(Bulk 1) techBlitz (2).pdf'
    excel_path = r'C:\Users\dhany\Downloads\Participants List.xlsx'
    output_dir = r'C:\Users\dhany\Downloads\Participants_check'

    # Read the Excel file
    df = pd.read_excel(excel_path)

    # Assuming the Excel file has columns named 'FirstName' and 'LastName' with the desired PDF names
    names_list = (df['Member Name'] + '_' + df['USN']).tolist()

    # Print number of names for debugging
    print(f"Number of names in Excel: {len(names_list)}")

    # Split the PDF and rename the files
    split_pdf(input_pdf_path, output_dir, names_list)


if __name__ == "__main__":
    main()
