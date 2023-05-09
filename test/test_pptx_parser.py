import unittest
from pptx_parser import PptxParser

class TestPptxParser(unittest.TestCase):
    def test_parse_presentation(self):
        pptx_parser = PptxParser("./files/presentation_for_tst.pptx")
        slides_dict = pptx_parser.parse_presentation()

        # Expected dictionary based on the test PowerPoint file
        expected_dict = {
            1: "PE format structure and explanation",
            2: "IDA -  tool for reverse exe file"  # Keep the extra space here
        }

        self.assertDictEqual(slides_dict, expected_dict)

if __name__ == '__main__':
    unittest.main()
