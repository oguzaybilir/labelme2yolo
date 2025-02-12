import unittest
from json_to_yolo_v1 import JsonToYolo

class TestJsonToYolo(unittest.TestCase):
    
    def setUp(self):
        self.converter = JsonToYolo(path="dummy-path",
                                    target="dummy-target",
                                    task="detection")
    
    def test_is_bbox_or_polygon_bbox(self):
        # Bounding box için bir örnek
        label_bbox = "0 0.50 0.5 0.2 0.3"  # class_id, x_center, y_center, width, height
        output = self.converter._is_bbox_or_polygon(label_bbox)
        
        # Beklenen sonuç: Detection (BBox)
        self.assertEqual(output, "Detection (BBox)")  # ✅ Doğru test

    def test_is_bbox_or_polygon_polygon(self):
        # En az 4 noktalı (8 değer) bir polygon kullanmalıyız
        label_polygon = "1 0.1 0.1 0.2 0.2 0.3 0.3"  # 3 nokta
        output = self.converter._is_bbox_or_polygon(label_polygon)

        # Beklenen sonuç: Segmentation (Polygon)
        self.assertEqual(output, "Segmentation (Polygon)")  # ✅ Doğru test



if __name__ == "__main__":
    unittest.main()
