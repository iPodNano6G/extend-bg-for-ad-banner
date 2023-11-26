from google.cloud import vision

class ObjectDetector:
    @classmethod
    def detect_objects(cls, image_bytes):
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
    
    @classmethod
    def detect_texts(cls, image_bytes):
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_bytes)
        responses = client.text_detection(image=image)
        texts = responses.text_annotations
        fullText = responses.full_text_annotation.text
        results = []
        for text in texts:
            result = {}
            result["description"] = text.description
            left = text.bounding_poly.vertices[0].x
            top = text.bounding_poly.vertices[0].y
            right = text.bounding_poly.vertices[2].x
            bottom = text.bounding_poly.vertices[2].y
            result.update({
                "left": left,
                "top": top,
                "right": right,
                "bottom": bottom 
            })
            results.append(result)

        return results, fullText

