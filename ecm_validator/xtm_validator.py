from collections import deque


def topological(graph):
	gray, black = 0, 1
	order, enter, state = deque(), set(graph), {}
	
	def dfs(node):
		state[node] = gray
		for k in graph.get(node, ()):
			sk = state.get(k[1], None)
			if sk == gray:
				raise CycleException((node, k[1]))
			if sk == black:
				continue
			enter.discard(k[1])
			dfs(k[1])
		order.appendleft(node)
		state[node] = black
	
	while enter:
		dfs(enter.pop())
	return order


class ValidationError(Exception):
	pass


class CycleException(ValidationError):
	def __init__(self, value):
		self.message = "CycleException: Cycle between nodes %s and %s" % (str(value[0]), str(value[1]))
	
	def __str__(self):
		return self.message


# TODO: define Exceptions behaviour
class NotUniqueException(ValidationError):
	pass


class NotALeafException(ValidationError):
	pass


class IsItemException(ValidationError):
	pass


class PrimaryInboundException(ValidationError):
	def __init__(self):
		self.message = "Inbound Exception"
	
	def __str__(self):
		return self.message
		
class PrimaryUnReqException(ValidationError):
	def __init__(self):
		self.message = "UnReq Exception"
	
	def __str__(self):
		return self.message
	
class SecondaryNoInboundException(ValidationError):
	def __init__(self):
		self.message = "Inbound Exception"
	
	def __str__(self):
		return self.message
	
def list_children(root, name):
	return filter(lambda child: child.name == name, root.children)

# TODO: Occurences handling
def validate_constraints(header):
	"""Validates DOM starting from header.root
	:param header -- Xml header returned from xml_parse
	:returns True -- if no exception occurs
	"""
	
	class Association:
		def __init__(self, root):
			self.relation_type = Type(root)
			roles = list_children(root, "role")
			self.roles = (Role(roles[0]), Role(roles[1]))
			
	class InstanceOf:
		def __init__(self, root):
			self.topic_refs = [TopicRef(t_ref) for t_ref in root.children]
		
	class TopicRef:
		def __init__(self, root):
			self.topic_ref = root.attributes['href']
			
		def __str__(self):
			return str(topics.get(self.topic_ref.strip('#')))
			
		def __repr__(self):
			return self.topic_ref.strip('#')
			
		def __hash__(self):
			return hash(self.topic_ref)

		def __eq__(self, other):
			if not isinstance(other, type(self)): return NotImplemented
			return self.topic_ref == other.topic_ref
		
	class Type(TopicRef):
		def __init__(self, root):
			TopicRef.__init__(self, list_children(root, "type")[0].children[0])
		
	class Role(TopicRef):
		def __init__(self, root):
			TopicRef.__init__(self, list_children(root, "topicRef")[0])
			self.role_type = Type(root)
			
	tree = header.root
	topics = {}  # dictionary topicid, topicname
	topics_occurrences = {}
	adj_list = {}  # dictionary node, adjacencies

	primary_notion_topic_id = ''
	secondary_notion_topic_id = ''
	primary_secondary_notions = {"Primary Notion": [], "Secondary Notion": []}

	# select all the children nodes
	topic_nodes = filter(lambda node: node.name == "topic", tree.children)
	for topic in topic_nodes:
		topic_id = topic.attributes.get('id')
		# selects the "name" node among the children nodes of "topic"
		name_node = list_children(topic, "name")
		occurrences = list_children(topic, "occurrence")
		instance_node = list_children(topic, "instanceOf")
		
		if occurrences:
			if topics_occurrences.get(topic_id):
				topics_occurrences[topic_id] += [Type(occurrence) for occurrence in occurrences]
			else:
				topics_occurrences[topic_id] = [Type(occurrence) for occurrence in occurrences]
		
		if instance_node:
			instances = InstanceOf(instance_node[0])
			for ref in instances.topic_refs:
				if primary_notion_topic_id == ref.topic_ref.strip('#'):
					primary_secondary_notions["Primary Notion"].append(topic_id)
				elif secondary_notion_topic_id == ref.topic_ref.strip('#'):
					primary_secondary_notions["Secondary Notion"].append(topic_id)
		# checks if there's a "name" node
		if name_node:
			# selects the "value" node
			value = list_children(name_node[0], "value")[0].children[0]
			if value == 'Primary Notion':
				primary_notion_topic_id = topic_id
			elif value == 'Secondary Notion':
				secondary_notion_topic_id = topic_id
			# creates the entry in the map
			topics[topic_id] = value

	# il grafo non presenta cicli
	# il nodo g con ruolo di deepening non ha archi in uscita
	# il nodo q con ruolo di individual non ha archi in uscita che non siano "is_rel"
	
	rel_type_aux_dict = {
		"is_rel": ['linked 1', 'linked 2'],
		"is_sug": ['main', 'deepening'],
		"is_req": ['prerequisite', 'subsidiary'],
		"is_item": ['general', 'individuals']
	}
	
	associations = [Association(_rel) for _rel in list_children(tree, "association")]
	
	# for each graph relation create a representation in an adjacency list
	for relation in filter(lambda ass: str(ass.relation_type) in rel_type_aux_dict.keys(), associations):
		
		# if one of the topics is the generic Primary Notion or Secondary Notion discard the association
		if any([str(_role) in ['Primary Notion', 'Secondary Notion'] for _role in relation.roles]):
			continue
		
		# Establish the roles in the associations to give a direction to the adjacency list
		
		def fill_adj_list(rel_type):
			role_1 = filter(lambda role: str(role.role_type) == rel_type_aux_dict[rel_type][0], relation.roles)[0]
			role_2 = filter(lambda role: str(role.role_type) == rel_type_aux_dict[rel_type][1], relation.roles)[0]
			
			if role_1 not in adj_list:
				adj_list[role_1] = []
			if role_2 not in adj_list:
				adj_list[role_2] = []
			adj_list[role_1].append((rel_type, role_2))
		
		fill_adj_list(str(relation.relation_type))
	
	# print adj_list
	# print topics_occurrences
	# print primary_secondary_notions
	
	top_order = topological(adj_list)
	
	supposed_secondary = set([])
	
	for elem in top_order:
		#if element has not been put among the secondary notions by a previous one, it is a primary notion
		if elem not in supposed_secondary:
			#This should be a Primary Notion, if it's not on the list of Primary Notions raise error as it is a Secondary notion with no inbound arcs
			if repr(elem) not in set(primary_secondary_notions["Primary Notion"]):
				raise SecondaryNoInboundException
			#If a Primary notion has an outbound arc that is not Is required raise Error
			if filter(lambda (rel,target) : rel != 'is_req',adj_list[elem]):
				raise PrimaryUnReqException
			#print filter(lambda a: a, topics_occurrences[repr(elem)]) da utilizzare sui vincoli delle occurrence
		for (rel, target) in adj_list[elem]:
			supposed_secondary.add(target)
			#This should be a Secondary Notion, if it's not on the list of Secondary Notions raise error as it is a Primary notion with inbound arcs
			if repr(target) not in set(primary_secondary_notions["Secondary Notion"]):
				raise PrimaryInboundException
			#print filter(lambda a: a, topics_occurrences[repr(target)])
		
		
	# check constraints on those lists:
	
	for k, v in adj_list.iteritems():
		# if the size of an entry of the adjacency list is greater than
		# the set based off the 2nd member of the tuple (destination of the edge)
		# then that means there's at least 1 relation which has the same destination
		if len(set([y for x, y in v])) < len(v):
			raise NotUniqueException(k)
		# given a certain entry `v` of the adjacency list, choose a sublist `sub_v` containing only "is_sug" relations,
		# then, for each element of `sub_v`, if the size of the adjacency list of this element is different than zero,
		# add it to the output.
		# If the output is not empty, that means at least 1 element of `sub_v` is not a leaf
		if filter(lambda (rel, dest): rel == "is_sug" and len(adj_list[dest]) != 0, v):
			raise NotALeafException()
		# given a certain entry `v` of the adjacency list, choose a sublist `sub_v` containing only "is_item" relations,
		# then, for each element `e` of `sub_v`, let adj_list[e.dest] as `l`, create a list containing only the "is_rel"
		# relations `l_is_rel`. If `l_is_rel` has a different size than `l`, then add it to the output.
		# If the output is not empty, that means at least 1 element of `sub_v` has at least 1 relation which isn't "is_rel"
		if filter(lambda (rel, dest): rel == "is_item" and
					len([(re, des) for (re, des) in adj_list[dest] if re != "is_rel"]) != 0, v):
			raise IsItemException()
