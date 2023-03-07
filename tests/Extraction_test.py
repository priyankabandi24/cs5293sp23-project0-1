# import unittest
# import os
# import project0.GPTmain
#
# class TestExtractInfoFromPDF(unittest.TestCase):
#     def setUp(self):
#         self.filename ="test.pdf"
#
#
#     def test_extract_info_from_pdf_success(self):
#
#         current_dir = os.getcwd()
#
#         full_path = os.path.join(current_dir, self.filename)
#
#         info = project0.GPTmain.extract_info_from_pdf(full_path)
#         assert len(info) > 2
#         self.assertEqual(info[1]["date_time"], "10/6/2022 0:22")
#         self.assertEqual(info[1]["incident_number"], "2022-00062137")
#         self.assertEqual(info[1]["nature"], "Traffic Stop")
#         self.assertEqual(info[1]["location"], "12THAVESE/ELINDSEYST")
#         self.assertEqual(info[1]["origin"], "OK0140200")



import os
import pytest
from project0.main import extract_info_from_pdf

@pytest.fixture
def pdf_file_path():
    return os.path.join(os.getcwd(), "test.pdf")

def test_extract_info_from_pdf_success(pdf_file_path):
    info = extract_info_from_pdf(pdf_file_path)
    assert len(info) > 2
    assert info[1]["date_time"] == "10/6/2022 0:22"
    assert info[1]["incident_number"] == "2022-00062137"
    assert info[1]["nature"] == "Traffic Stop"
    assert info[1]["location"] == "12THAVESE/ELINDSEYST"
    assert info[1]["origin"] == "OK0140200"

