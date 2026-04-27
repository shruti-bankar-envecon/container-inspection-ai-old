# core/llm_validator.py
import json
import base64
import cv2
from openai import OpenAI

class LLMValidator:
    def __init__(self, config):
        self.config = config['llm']
        self.vision_config = config.get('vision_analysis', {})
        if not self.config.get('api_key'):
            self.client = None
            print("WARNING: OpenAI client not initialized.")
        else:
            self.client = OpenAI(api_key=self.config['api_key'])

    def validate_and_correct_ocr(self, raw_text: str, image_bytes: bytes = None) -> dict:
        """Enhanced OCR validation using GPT-5 with improved accuracy"""
        if not self.client:
            print("INFO: LLM validation skipped. Returning mock data.")
            return {
                "container_number": "ATRU8161258",
                "container_type": "40ft Standard",
                "gross_weight": 30480,
                "tare_weight": 3800,
                "net_weight": 26680,
                "volume": 67.7,
                "max_gross_weight": 30480,
                "owner": "N/A",
                "certification_valid": True,
                "confidence_score": 0.95
            }

        # If image is provided, use vision model to extract container number directly
        if image_bytes:
            try:
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                vision_prompt = """
                Analyze this shipping container image and extract the container number.
                
                CRITICAL: Look for the container number which follows ISO 6346 format:
                - 4 letters (owner code) + 6 digits + 1 check digit
                - Examples: CPIU1811772, MSCU1234567, TEMU9876543
                
                The container number is usually painted in large letters on the container.
                In this image, look carefully at all visible text on the container.
                
                Return ONLY a JSON object:
                {
                  "container_number": "XXXX1234567",
                  "container_type": "20ft/40ft/45ft Standard/High Cube/etc",
                  "confidence_score": 0.0-1.0
                }
                """
                
                response = self.client.chat.completions.create(
                    model=self.vision_config.get('model', 'gpt-4o'),
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": vision_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                                }
                            ]
                        }
                    ],
                    temperature=0.0,
                    response_format={"type": "json_object"}
                )
                
                vision_result = json.loads(response.choices[0].message.content)
                if vision_result.get('container_number') and vision_result['container_number'] != "N/A":
                    return vision_result
            except Exception as e:
                print(f"ERROR: Vision-based container extraction failed: {e}")

        # Fallback to text-based extraction
        prompt = self.config['prompt_template'].format(raw_text=raw_text)
        try:
            response = self.client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config['temperature'],
                response_format={"type": "json_object"}
            )
            corrected_json = response.choices[0].message.content
            return json.loads(corrected_json)
        except Exception as e:
            print(f"ERROR: GPT-5 API call failed: {e}")
            return {
                "error": "LLM validation failed", 
                "container_number": "N/A",
                "confidence_score": 0.0
            }

    def analyze_image_damage(
        self,
        image_bytes: bytes,
        image_shape: tuple = None,
        profile: str = None,
        model_override: str = None,
        **kwargs,
    ) -> dict:
        """Use GPT-5 Vision for direct image damage analysis.

        Args:
            image_bytes: JPEG-encoded image bytes.
            image_shape: Optional (height, width) tuple used to guide bbox coordinates.
            profile: Optional damage prompt profile (e.g. "yolo", "insurance"). Currently
                     used only for prompt selection; safe to ignore if not configured.
            model_override: Optional model name that, when provided, overrides the
                            default vision model from config (used for fast/second-pass).
        """
        if not self.client:
            print("INFO: GPT-5 Vision analysis skipped. Returning mock data.")
            return {
                "damages": [],
                "overall_condition": "Good",
                "structural_integrity": "Intact",
                "safety_concerns": [],
                "maintenance_recommendations": ["Regular inspection recommended"],
                "estimated_repair_cost": 0,
                "confidence_score": 0.85
            }

        # Encode image to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Add image dimensions to prompt if available
        dimension_info = ""
        if image_shape:
            height, width = image_shape[:2]
            dimension_info = f"\n\nIMAGE DIMENSIONS: {width}x{height} pixels. When providing bounding boxes, use coordinates relative to these dimensions. For example, if a damage is in the center, the bbox might be around [{width//4}, {height//4}, {width//2}, {height//2}]."
        
        try:
            # Allow different prompt templates per profile if configured
            if profile:
                profile_key = f"damage_detection_prompt_{str(profile).lower()}"
                prompt_base = self.vision_config.get(profile_key, self.vision_config.get('damage_detection_prompt', ''))
            else:
                prompt_base = self.vision_config.get('damage_detection_prompt', '')

            prompt_text = prompt_base + dimension_info

            # Allow pipeline to override the model (e.g., fast model or second-pass model)
            model_name = model_override or self.vision_config.get('model', 'gpt-4o')
            
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt_text
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=self.vision_config.get('temperature', 0.0),
                response_format={"type": "json_object"}
            )
            
            analysis_json = response.choices[0].message.content
            return json.loads(analysis_json)
            
        except Exception as e:
            print(f"ERROR: GPT-5 Vision analysis failed: {e}")
            return {
                "error": "Vision analysis failed",
                "damages": [],
                "overall_condition": "Unknown",
                "confidence_score": 0.0
            }

    def enhanced_damage_analysis(self, image_bytes: bytes, initial_damages: list) -> dict:
        """Enhanced damage analysis with GPT-5 for detailed assessment"""
        if not self.client:
            print("INFO: Enhanced analysis skipped. Returning basic analysis.")
            return {
                "enhanced_damages": initial_damages,
                "repair_recommendations": [],
                "cost_breakdown": {},
                "safety_assessment": "Standard",
                "compliance_status": "Unknown"
            }

        # Encode image to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        enhanced_prompt = f"""
        {self.vision_config.get('enhanced_analysis_prompt', '')}
        
        INITIAL DAMAGE DETECTIONS:
        {json.dumps(initial_damages, indent=2)}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.vision_config.get('model', 'gpt-5-vision'),
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": enhanced_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=self.vision_config.get('temperature', 0.0),
                response_format={"type": "json_object"}
            )
            
            enhanced_analysis = response.choices[0].message.content
            return json.loads(enhanced_analysis)
            
        except Exception as e:
            print(f"ERROR: Enhanced analysis failed: {e}")
            return {
                "error": "Enhanced analysis failed",
                "enhanced_damages": initial_damages
            }