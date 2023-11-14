from google.cloud import vision

import json

class ObjectDetector:
    def detect_objects(image_bytes):
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_bytes)
        objects = client.object_localization(
            image=image).localized_object_annotations

        results = []
        for obj in objects:
            result = {}
            result["name"] = obj.name.lower()
            result["score"] = obj.score
            four_normalized_vertices_obj = obj.bounding_poly.normalized_vertices
            left = four_normalized_vertices_obj[0].x
            top = four_normalized_vertices_obj[0].y
            right = four_normalized_vertices_obj[2].x
            bottom = four_normalized_vertices_obj[2].y
            result.update({
                "left": left,
                "top": top,
                "right": right,
                "bottom": bottom 
            })
            results.append(result)

        return results
