#TODO : dataclass
class Pointer:

  def __init__(addr, port):
  # A Pointer consists of an addr / port pair
    self.addr = addr # integer (index on this.nodes where the target port is)
    self.port = port # integer (0, 1 or 2, representing the target port)

  def __str__(self):
    return self.addr + 'abc'[self.port]
  
  def __eq__(self, other):
    return other is not None and self.addr == self.addr and self.port == self.port


class Node:

  def __init__(label, ports):
  # A node consists of a label and an array with 3 ports 
    self.label = label # integer (this node's label)
    self.ports = ports # array with 3 pointers (this node's edges)

  def __str__(self):
    return '[' + this.label + '|' + this.ports[0].to_string() + ' ' + this.ports[1].to_string() + ' ' + this.ports[2].to_string() + ']'




class Net:
  # A net stores nodes (this.nodes), reclaimable memory addrs (this.freed) and active pairs (this.redex)
  def __init__():
    self.nodes = [] # nodes
    self.freed = [] # integers
    self.redex = [] # array of (integer, integer) tuples representing addrs

  # Allocates a new node, return its addr
  def alloc_node(self, label):

    # If there is reclaimable memory, use it
    if (self.freed.length > 0):
      addr = self.freed.pop()
    else: # Otherwise, extend the array of nodes
      self.nodes.push(null)
      addr = self.nodes.length - 1

    # Fill the memory with an empty node without pointers
    self.nodes[addr] = Node(label, [None, None, None]);
    return addr


  # Deallocates a node, allowing its space to be reclaimed
  def free_node(self, addr):
    self.nodes[addr] = null
    self.freed.push(addr)

  # Given a pointer to a port, returns a pointer to the opposing port
  def enter_port(self, ptr):
    if (self.nodes[ptr.addr] is not None):
      return self.nodes[ptr.addr].ports[ptr.port]
    else:
      return None

  # Connects two ports
  def link_ports(self, a_ptr, b_ptr):
    # Stores each pointer on its opposing port
    self.nodes[a_ptr.addr].ports[a_ptr.port] = b_ptr
    self.nodes[b_ptr.addr].ports[b_ptr.port] = a_ptr

    # If both are main ports, add this to the list of active pairs
    if (a_ptr.port == 0 and b_ptr.port == 0):
      self.redex.push([a_ptr.addr, b_ptr.addr])

  # Disconnects a port, causing both sides to point to themselves
  def unlink_port(self, a_ptr):
    b_ptr = this.enter_port(a_ptr);
    if (self.enter_port(b_ptr).equal(a_ptr)):
      self.nodes[a_ptr.addr].ports[a_ptr.port] = a_ptr
      self.nodes[b_ptr.addr].ports[b_ptr.port] = b_ptr

  # Rewrites an active pair
  def rewrite(self, [a_addr, b_addr]):
    a_node = self.nodes[a_addr]
    b_node = self.nodes[b_addr]

    # If both nodes have the same label, connects their neighbors
    if (a_node.label == b_node.label):
      a_aux1_dest = this.enter_port(Pointer(a_addr, 1))
      b_aux1_dest = this.enter_port(Pointer(b_addr, 1))
      self.link_ports(a_aux1_dest, b_aux1_dest)
      a_aux2_dest = this.enter_port(Pointer(a_addr, 2))
      b_aux2_dest = this.enter_port(Pointer(b_addr, 2))
      self.link_ports(a_aux2_dest, b_aux2_dest)

    # Otherwise, the nodes pass through each-other, duplicating themselves
    else:
      p_addr = this.alloc_node(b_node.label)
      q_addr = this.alloc_node(b_node.label)
      r_addr = this.alloc_node(a_node.label)
      s_addr = this.alloc_node(a_node.label)
      self.link_ports(Pointer(r_addr, 1), Pointer(p_addr, 1))
      self.link_ports(Pointer(s_addr, 1), Pointer(p_addr, 2))
      self.link_ports(Pointer(r_addr, 2), Pointer(q_addr, 1))
      self.link_ports(Pointer(s_addr, 2), Pointer(q_addr, 2))
      self.link_ports(Pointer(p_addr, 0), self.enter_port(Pointer(a_addr, 1)))
      self.link_ports(Pointer(q_addr, 0), self.enter_port(Pointer(a_addr, 2)))
      self.link_ports(Pointer(r_addr, 0), self.enter_port(Pointer(b_addr, 1)))
      self.link_ports(Pointer(s_addr, 0), self.enter_port(Pointer(b_addr, 2)))

    # Deallocates the space used by the active pair
    for (var i = 0; i < 3; i++):
      self.unlink_port(Pointer(a_addr, i))
      self.unlink_port(Pointer(b_addr, i))
    self.free_node(a_addr)
    if (a_addr !== b_addr):
      self.free_node(b_addr)

  # Rewrites active pairs until none is left, reducing the graph to normal form
  # This could be performed in parallel. Unreachable data is freed automatically.
  def reduce(self):
    rewrite_count = 0
    while (this.redex.length > 0):
      self.rewrite(this.redex.pop())
      rewrite_count += 1
    return {rewrites: rewrite_count}
  }

  # Rewrites active pairs lazily. Lazy reductions avoid wasting work and
  # allows recursive terms, but requires GC and enforces sequentiality.
  def reduce_lazy(self):
    warp = []
    exit = []
    next = this.enter_port(Pointer(0, 1))
    prev = null
    back = null
    rwts = 0
    while (next.addr > 0 || warp.length > 0):
      next = next.addr == 0 ? this.enter_port(warp.pop()) : next
      prev = this.enter_port(next)
      if (next.port == 0 and prev.port == 0):
        back = this.enter_port(Pointer(prev.addr, exit.pop()))
        self.rewrite([prev.addr, next.addr])
        next = this.enter_port(back)
        ++rwts
      else if (next.port == 0):
        warp.push(Pointer(next.addr, 2))
        next = this.enter_port(Pointer(next.addr, 1))
      else:
        exit.push(next.port)
        next = this.enter_port(Pointer(next.addr, 0))
    return {rewrites: rwts}

  def __str__(self):
    text = '';
    for (var i = 0; i < this.nodes.length; i++):
      if (this.nodes[i] !== null):
        text += i + ': ' + this.nodes[i].to_string() + '\n';
      else:
        text += i + ': ' + null + '\n';
    return text;
    
    

