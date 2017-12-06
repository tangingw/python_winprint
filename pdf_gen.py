import PyPDF2


def parser(num_range):

    """
    This function parses the num_range to num list in
    reversed order

    Args:
        num_range(str): num ranges in the format of x-y

    Return:
        list: The reverse list of the num_range

    Example:
        print parser(20-25)

        return [24, 23, 22, 21, 20, 19]

    """

    index_list = [int(item) for item in num_range.split("-")]

    #Pages range in reversed order
    return [i for i in range(index_list[0]-1, index_list[1])][::-1]


def print_pdf(input_file, output_file, page_range):

    """
    This function generates a new pdf with desired output filename,
    by inserting the input filename and page range that you want to print

    Args:
        input_file(str): input pdf filename
        output_file(str): output pdf filename
        page_range(str): page range in the format of x-y

    Returns:
        void

    Example:

       print_pdf("/foo/bar.pdf", "/foo/new_bar.pdf", 20-25)

    """
    pdf_file = open(input_file, "r")

    read_pdf = PyPDF2.PdfFileReader(pdf_file, strict=False)
    #meta_data = read_pdf.documentInfo

    try:

        new_pdf = open(output_file, "w")
        write_pdf = PyPDF2.PdfFileWriter()
        #write_pdf.addMetadata(meta_data)

        for item in parser(page_range):

            write_pdf.insertPage(read_pdf.getPage(item))

        write_pdf.write(new_pdf)
        print "%s Generated" % output_file

    except IndexError:

        print "Page not Found!"
