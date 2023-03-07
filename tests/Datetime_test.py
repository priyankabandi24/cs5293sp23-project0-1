# import unittest
# import os
# import project0.GPTmain
#
# class TestDownloadPDF(unittest.TestCase):
#     def test_download_pdf_success(self):
#         url = "https://www.normanok.gov/sites/default/files/documents/2022-10/2022-10-06_daily_incident_summary.pdf"
#         filename = project0.GPTmain.download_pdf(url)
#         self.assertTrue(os.path.exists(filename))
#         os.remove(filename)
#
#     def test_download_pdf_failure(self):
#         url = "https://www.normanok.gov/sites/default/files/documents/2022-10/2022-10-06_daily_incident_summary_invalid_url.pdf"
#         with self.assertRaises(Exception):
#             project0.GPTmain.download_pdf(url)

import os
import project0.main
import pytest

def test_download_pdf_success():
    url = "https://www.normanok.gov/sites/default/files/documents/2022-10/2022-10-06_daily_incident_summary.pdf"
    filename = project0.main.download_pdf(url)
    assert os.path.exists(filename)
    os.remove(filename)

def test_download_pdf_failure():
    url = "https://www.normanok.gov/sites/default/files/documents/2022-10/2022-10-06_daily_incident_summary_invalid_url.pdf"
    with pytest.raises(Exception):
        project0.main.download_pdf(url)
