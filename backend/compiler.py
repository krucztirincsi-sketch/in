from backend.atomic_functions import AVAILABLE_FUNCTIONS

class SLCCompiler:
    def __init__(self):
        self.functions = AVAILABLE_FUNCTIONS

    def compile(self, execution_plan: dict, raw_data: list) -> str:
        """
        Executes the logic plan step by step and assembles the HTML string.
        """
        step_outputs = {}
        ui_elements = []

        steps = execution_plan.get("steps", [])

        for step in steps:
            step_id = step.get("id")
            func_name = step.get("function")
            inputs = step.get("inputs", {})
            is_ui = step.get("is_ui", False)

            # Resolve inputs
            resolved_inputs = {}
            for key, val in inputs.items():
                if isinstance(val, str) and val == "$RAW_DATA":
                    resolved_inputs[key] = raw_data
                elif isinstance(val, str) and val.startswith("$STEP_"):
                    ref_id = val.replace("$STEP_", "")
                    resolved_inputs[key] = step_outputs.get(ref_id)
                else:
                    resolved_inputs[key] = val

            # Execute the function
            if func_name not in self.functions:
                raise ValueError(f"Unknown atomic function: {func_name}")

            func = self.functions[func_name]
            try:
                result = func(**resolved_inputs)
                step_outputs[step_id] = result

                if is_ui:
                    ui_elements.append(result)
            except Exception as e:
                # In SLC, we don't crash, we try to render the error visually as an atomic block
                error_html = f"""
                <div class="alert alert-danger" role="alert">
                  <strong>Compiler Logic Error in step '{step_id}' ({func_name}):</strong> {str(e)}
                </div>
                """
                ui_elements.append(error_html)

        # Assemble the final "Micro-App" UI
        # We wrap the UI elements in a simple Bootstrap container for styling
        assembled_html = "\n".join(ui_elements)

        return assembled_html
