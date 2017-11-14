from OpenGL.GL import *
from OpenGL.GLU import *

def load_and_compile_shader(shader_type, name):
	source_code = None
	with open(name) as f:
		source_code = f.readlines()	
	shader_id = glCreateShader(shader_type)
	glShaderSource(shader_id, source_code)
	glCompileShader(shader_id)
	# get debug info
	message = glGetShaderInfoLog(shader_id)
	if message:
		raise Exception("[Shader compilation failed] \n" + message + "\n Exiting...")
	return shader_id
	
	
def create_program(vertex_file = None, fragment_file = None, tess_con_file = None, tess_eval_file = None, compute_file = None):
	'''
	Possible function calls:
	1. vertex_file, fragment_file, tess_con_file and tess_eval_file are not None
	2. vertex_file and fragment_file are not None
	3. compute_file is not None
	'''
	program = glCreateProgram()
	if vertex_file is not None and fragment_file is not None:
		vertex_shader_id    = load_and_compile_shader(GL_VERTEX_SHADER, vertex_file)
		fragment_shader_id  = load_and_compile_shader(GL_FRAGMENT_SHADER, fragment_file)
		glAttachShader(program, vertex_shader_id)
		glAttachShader(program, fragment_shader_id)
		if tess_con_file is not None and tess_eval_file is not None:
			tess_eval_id = load_and_compile_shader(GL_TESS_EVALUATION_SHADER, tess_eval_file)
			tess_con_id = load_and_compile_shader(GL_TESS_CONTROL_SHADER, tess_con_file)
			glAttachShader(program, tess_eval_id)
			glAttachShader(program, tess_con_id)
		# free up the now-unnecessary shader binaries
		glDeleteShader(vertex_shader_id)
		glDeleteShader(fragment_shader_id)
		if tess_eval_file is not None and tess_con_file is not None:
			glDeleteShader(tess_eval_id)
			glDeleteShader(tess_con_id)
	else:
		compute_shader_id = load_and_compile_shader(GL_COMPUTE_SHADER, compute_file)
		glAttachShader(program, compute_shader_id)
		glDeleteShader(compute_shader_id)
	glLinkProgram(program)
	# get debug info
	message = glGetProgramInfoLog(program)
	if message:
		print("[Shader linking failed]")
		print(message)
	glUseProgram(0)
	return program