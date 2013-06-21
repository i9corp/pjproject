# $Id$

#!/usr/bin/python

# import re
import sys #, os, traceback
from collections import OrderedDict
from pycparser import parse_file, c_ast, c_generator

# Settings.
PJ_ROOT_PATH = "../../../"
SOURCE_PATH  = PJ_ROOT_PATH + "pjsip/include/pjsua-lib/pjsua.h"
#SOURCE_PATH  = PJ_ROOT_PATH + "pjlib-util/include/pjlib-util/scanner.h"
#SOURCE_PATH  = PJ_ROOT_PATH + "pjlib/include/pj/types.h"

# CPP (C preprocessor) settings, CPP is needed by pycparser.
CPP_PATH     = 'C:/devs/bin/cpp.exe' if sys.platform == 'win32' else 'cpp'
CPP_CFLAGS   = [
	r'-DPJ_AUTOCONF',
	r'-DCC_DUMMY',
	r'-Djmp_buf=int',
	r'-IC:/devs/tools/pycparser/utils/fake_libc_include',
	"-I" + PJ_ROOT_PATH + "pjlib/include",
	"-I" + PJ_ROOT_PATH + "pjlib-util/include",
	"-I" + PJ_ROOT_PATH + "pjnath/include",
	"-I" + PJ_ROOT_PATH + "pjmedia/include",
	"-I" + PJ_ROOT_PATH + "pjsip/include"
	]

# Any type/func names without this prefix will be excluded from the generated SWIG interface,
# e.g: int, void.
BASE_PREFIX = 'pj'

# Any type/func names with this prefix will be treated as part of main module, i.e: they will
# always be included in the generated SWIG interface, and will be used as starting point in
# tracing dependencies (e.g: as struct pjsua_acc_config is part of main module, any types used
# in its struct member, such as pj_str_t, pjsip_hdr, pj_bool_t, etc, will be included too).
MODULE_PREFIX = 'pjsua_'
#MODULE_PREFIX = 'pj'

# If true, video related declarations (anything has '_vid_') will be removed, as long as not
# used by main module (e.g: pjmedia_vid_dev_index type is used by pjsua_acc_config, so it won't
# be removed).
NO_VIDEO = True

FORCE_STRUCT_AS_OPAQUE = [
	'pj_pool_t',
	'pj_stun_msg',
	'pj_pool_factory',
	'pjsip_hdr_vptr',
	'pjsip_tpfactory',
	'pjsip_transport',
	'pjsip_tx_data_op_key',
	'pjsip_rx_data_op_key',
	'pjsip_module',
	'pjmedia_port',
	'pjmedia_transport',
	'pjsua_media_transport',
	'pjsua_callback'
]

FORCE_EXPORT = [
	#'pj_str' # plain export result doesn't work!
]

class MyGen(c_generator.CGenerator):
    
    def __init__(self, ast):
        super(MyGen, self).__init__()
        self.ast = ast
        self.nodes = OrderedDict()
	self.deps = list()
	self.deps_pending = list()
	self.deps_frozen = False

	# Generate nodes map (name -> node instances)
        for ext in self.ast.ext:
	    name = self._get_node_name(ext)
            if name and not name.startswith(BASE_PREFIX):
	        continue
	
	    if name in self.nodes:
	        self.nodes[name].append(ext)
                # always put typedef later, swig issue
	        if isinstance(self.nodes[name][0], c_ast.Typedef):
		    self.nodes[name].reverse()
	    else:
	        self.nodes[name] = [ext]
		
        # Generate dependencies, they are all APIs to be exported
        for name in self.nodes.keys():
	    if (not name) or \
	       ((name in FORCE_EXPORT or name.startswith(MODULE_PREFIX)) \
	              and self._check_video(name)):
	        self._add_dep(name)
	self.deps_frozen = True
	
    # Override visit_IdentifierType() to collect "node name" and generate dependencies
    # from this node's children
    def visit_IdentifierType(self, n):
	if not self.deps_frozen:
	    for name in n.names: self._add_dep(name)
        return ' '.join(n.names)

    def _check_video(self, name):
	if NO_VIDEO and name and ((name.find('_vid_') > 0) or (name.find('_video_') > 0)):
	    return False
	return True
    
    def _get_node_name(self, node):
        s = getattr(node, 'name', None)
	if s:
	    return s
	if isinstance(node, c_ast.FuncDef):
	    return self._get_node_name(node.decl)
	ss = getattr(node, 'names', None)
	if ss:
	    s = ' '.join(ss)
	    return s
	if getattr(node, 'type', None):
	    return self._get_node_name(node.type)
	return s

    # Trace node dependencies by recursively inspecting its children.
    # The node itself and all its children will be listed in 'deps'.
    def _add_dep(self, name):
        if (name and not name.startswith(BASE_PREFIX)) or \
	    name in self.deps or name in self.deps_pending:
	    return
	    
	if name in FORCE_STRUCT_AS_OPAQUE:
	    self.deps.append(name)
	    return
	    
	self.deps_pending.append(name)
	for node in self.nodes[name]:
	    self.visit(node)
	if not self.deps_pending.pop() == name:
	    print 'Error initializing dep!'
	    sys.exit(1)
	self.deps.append(name)
    	
    # Opaque struct is identified by empty struct member declaration.
    def _is_struct_opaque(self, node):
	if isinstance(node, c_ast.Typedef) and isinstance(node.type, c_ast.TypeDecl) and \
	   isinstance(node.type.type, c_ast.Struct) and node.type.type.decls == None:
	    return True
	elif isinstance(node, c_ast.Decl) and isinstance(node.type, c_ast.Struct) and \
	     node.type.decls == None:
	    return True
	return False

    # Check if the specified struct name is opaque. If it is, declare as zero member and
    # tell SWIG to omit ctor/dtor.
    def _process_opaque_struct(self, name, code):
        opaque = True
	if not (name in FORCE_STRUCT_AS_OPAQUE):
   	    for n in self.nodes[name]:
		if not self._is_struct_opaque(n):
		    opaque = False
		    break
	if opaque:
	    s = '%nodefaultctor ' + name + '; %nodefaultdtor ' + name + ';\n'
	    s += 'struct ' + name + ' {};\n'
	    return s

	# Remove "typedef struct/enum ..." without member decl (optional)
	if name:
	    code = code.replace('typedef struct '+name+' '+name+';\n', '', 1)
	    code = code.replace('typedef enum '+name+' '+name+';\n', '', 1)
	return code
	
    # Generate code from the specified node.
    def _print_node(self, node):
        s = ''
        if isinstance(node, c_ast.FuncDef):
	    s = self.visit(node)
        else:
	    s = self.visit(node)
	    if s: s += ';\n'
	return s

    def go(self):
	s = ''
	for name in self.deps:
	    ss = ''
	    for node in self.nodes[name]:
	        ss += self._print_node(node)
	    s += self._process_opaque_struct(name, ss)
	return s

# MAIN		
ast = parse_file(SOURCE_PATH, use_cpp=True, cpp_path=CPP_PATH, cpp_args=CPP_CFLAGS)
#ast.show(attrnames=True, nodenames=True)
#exit(0)

mygen = MyGen(ast)

#print 'Found ' + str(len(mygen.nodes)) + ' nodes:'
#for a, b in mygen.nodes.items():
#   print a + ':' + str(len(b))

#print '\n\nFound ' + str(len(mygen.deps)) + ' dependencies:'
#for d in mygen.deps:
#   print d

s = mygen.go()
print s