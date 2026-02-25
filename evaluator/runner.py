import subprocess, json, tempfile, os

class SafeRunner:
    def run(self, file_path, entrypoint, inputs):
        # Generamos el wrapper para ejecutar la función específica
        wrapper = f"""
import json, importlib.util
try:
    spec = importlib.util.spec_from_file_location("mod", r"{file_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    res = getattr(mod, "{entrypoint}")(**{inputs})
    print(json.dumps({{"s": True, "r": res}}))
except Exception as e:
    print(json.dumps({{"s": False, "e": str(e)}}))
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(wrapper)
            tmp_path = f.name
        
        try:
            # Forzamos python3 por compatibilidad Linux
            proc = subprocess.run(["python3", tmp_path], capture_output=True, text=True, timeout=5)
            data = json.loads(proc.stdout.strip())
            return data["s"], data.get("r"), data.get("e", "")
        except Exception as e:
            return False, None, str(e)
        finally:
            if os.path.exists(tmp_path): os.remove(tmp_path)