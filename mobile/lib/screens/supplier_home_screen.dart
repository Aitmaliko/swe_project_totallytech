import 'package:flutter/material.dart';
import '../models/user.dart';
import '../models/order.dart';
import '../models/link.dart';
import '../models/product.dart';
import '../services/order_service.dart';
import '../services/link_service.dart';
import '../services/product_service.dart';
import 'complaints_screen.dart';
import 'chat_screen.dart';

class SupplierHomeScreen extends StatefulWidget {
  final User user;

  const SupplierHomeScreen({super.key, required this.user});

  @override
  State<SupplierHomeScreen> createState() => _SupplierHomeScreenState();
}

class _SupplierHomeScreenState extends State<SupplierHomeScreen> {
  int _selectedIndex = 0;
  final _orderService = OrderService();
  final _linkService = LinkService();
  final _productService = ProductService();

  List<Order> _orders = [];
  List<Link> _pendingLinks = [];
  List<Link> _allLinks = [];
  List<Product> _products = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    try {
      final orders = await _orderService.getMyOrders();
      final pendingLinks = await _linkService.getPendingLinks();
      final allLinks = await _linkService.getMyLinks();
      final products = await _productService.getMyProducts();
      setState(() {
        _orders = orders;
        _pendingLinks = pendingLinks;
        _allLinks = allLinks;
        _products = products;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final screens = [
      _buildHomeTab(),
      _buildLinksTab(),
      _buildProductsTab(),
      _buildOrdersTab(),
      _buildChatsTab(),
      ComplaintsScreen(
        isSupplier: true,
        acceptedLinks: _allLinks.where((link) => link.status == 'accepted').toList(),
      ),
      _buildProfileTab(),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Supplier App'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _loadData),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : screens[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) =>
            setState(() => _selectedIndex = index),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.dashboard),
            label: 'Dashboard',
          ),
          NavigationDestination(icon: Icon(Icons.link), label: 'Links'),
          NavigationDestination(icon: Icon(Icons.inventory), label: 'Products'),
          NavigationDestination(
            icon: Icon(Icons.shopping_bag),
            label: 'Orders',
          ),
          NavigationDestination(icon: Icon(Icons.chat), label: 'Chats'),
          NavigationDestination(icon: Icon(Icons.report), label: 'Complaints'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }

  Widget _buildHomeTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          child: ListTile(
            title: Text('Welcome, ${widget.user.fullName}'),
            subtitle: Text('Role: ${widget.user.role}'),
          ),
        ),
        const SizedBox(height: 16),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Pending Link Requests',
                  style: TextStyle(fontSize: 14, color: Colors.grey),
                ),
                const SizedBox(height: 8),
                Text(
                  '${_pendingLinks.length}',
                  style: const TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: Colors.orange,
                  ),
                ),
              ],
            ),
          ),
        ),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Total Products',
                  style: TextStyle(fontSize: 14, color: Colors.grey),
                ),
                const SizedBox(height: 8),
                Text(
                  '${_products.length}',
                  style: const TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Total Orders',
                  style: TextStyle(fontSize: 14, color: Colors.grey),
                ),
                const SizedBox(height: 8),
                Text(
                  '${_orders.length}',
                  style: const TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildLinksTab() {
    return Stack(
      children: [
        _pendingLinks.isEmpty
            ? Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.check_circle, size: 64, color: Colors.green),
                    SizedBox(height: 16),
                    Text(
                      'No pending requests',
                      style: TextStyle(fontSize: 18, color: Colors.grey),
                    ),
                  ],
                ),
              )
            : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: _pendingLinks.length,
                itemBuilder: (context, index) {
                  final link = _pendingLinks[index];
                  return Card(
                    child: ListTile(
                      title: Text('Link Request #${link.id}'),
                      subtitle: Text('Consumer ID: ${link.consumerId}'),
                      trailing: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          IconButton(
                            icon: Icon(Icons.check, color: Colors.green),
                            onPressed: () => _approveLinkRequest(link.id),
                          ),
                          IconButton(
                            icon: Icon(Icons.close, color: Colors.red),
                            onPressed: () => _rejectLinkRequest(link.id),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
      ],
    );
  }

  Future<void> _approveLinkRequest(int linkId) async {
    try {
      await _linkService.updateLinkStatus(linkId, 'accepted', 'Approved');
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Link request approved!')));
      _loadData();
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  Future<void> _rejectLinkRequest(int linkId) async {
    try {
      await _linkService.updateLinkStatus(linkId, 'rejected', 'Rejected');
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Link request rejected')));
      _loadData();
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  Widget _buildProductsTab() {
    return Stack(
      children: [
        _products.isEmpty
            ? Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.inventory_2, size: 64, color: Colors.grey),
                    SizedBox(height: 16),
                    Text(
                      'No products yet',
                      style: TextStyle(fontSize: 18, color: Colors.grey),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Tap + to add a product',
                      style: TextStyle(color: Colors.grey),
                    ),
                  ],
                ),
              )
            : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: _products.length,
                itemBuilder: (context, index) {
                  final product = _products[index];
                  return Card(
                    child: ListTile(
                      title: Text(product.name),
                      subtitle: Text(
                        'Price: \$${product.price} | Stock: ${product.stockQuantity}',
                      ),
                      trailing: Icon(
                        product.isAvailable ? Icons.check_circle : Icons.cancel,
                        color: product.isAvailable ? Colors.green : Colors.red,
                      ),
                    ),
                  );
                },
              ),
        Positioned(
          right: 16,
          bottom: 16,
          child: FloatingActionButton(
            onPressed: _showAddProductDialog,
            child: Icon(Icons.add),
            tooltip: 'Add Product',
          ),
        ),
      ],
    );
  }

  void _showAddProductDialog() {
    final nameController = TextEditingController();
    final descriptionController = TextEditingController();
    final categoryController = TextEditingController();
    final unitController = TextEditingController();
    final priceController = TextEditingController();
    final stockController = TextEditingController();

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Add Product'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: nameController,
                decoration: InputDecoration(labelText: 'Name'),
              ),
              TextField(
                controller: descriptionController,
                decoration: InputDecoration(labelText: 'Description'),
                maxLines: 2,
              ),
              TextField(
                controller: categoryController,
                decoration: InputDecoration(labelText: 'Category'),
              ),
              TextField(
                controller: unitController,
                decoration: InputDecoration(labelText: 'Unit (e.g., kg)'),
              ),
              TextField(
                controller: priceController,
                decoration: InputDecoration(labelText: 'Price'),
                keyboardType: TextInputType.number,
              ),
              TextField(
                controller: stockController,
                decoration: InputDecoration(labelText: 'Stock Quantity'),
                keyboardType: TextInputType.number,
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              try {
                await _productService.createProduct(
                  name: nameController.text,
                  description: descriptionController.text,
                  category: categoryController.text,
                  unit: unitController.text,
                  price: double.parse(priceController.text),
                  stockQuantity: int.parse(stockController.text),
                );
                Navigator.pop(context);
                ScaffoldMessenger.of(
                  context,
                ).showSnackBar(SnackBar(content: Text('Product added!')));
                _loadData();
              } catch (e) {
                ScaffoldMessenger.of(
                  context,
                ).showSnackBar(SnackBar(content: Text('Error: $e')));
              }
            },
            child: Text('Add'),
          ),
        ],
      ),
    );
  }

  Widget _buildOrdersTab() {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _orders.length,
      itemBuilder: (context, index) {
        final order = _orders[index];
        return Card(
          child: ListTile(
            title: Text('Order #${order.id}'),
            subtitle: Text('Total: \$${order.totalAmount.toStringAsFixed(2)}'),
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(order.status),
                if (order.status == 'pending')
                  IconButton(
                    icon: Icon(Icons.check, color: Colors.green),
                    onPressed: () => _acceptOrder(order.id),
                  ),
              ],
            ),
          ),
        );
      },
    );
  }

  Future<void> _acceptOrder(int orderId) async {
    try {
      await _orderService.updateOrderStatus(
        orderId,
        'accepted',
        'Accepted by supplier',
      );
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Order accepted!')));
      _loadData();
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  Widget _buildChatsTab() {
    // Filter only accepted links for chat
    final acceptedLinks = _allLinks.where((link) => link.status == 'accepted').toList();
    
    if (acceptedLinks.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.chat_bubble_outline, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text(
              'No active chats',
              style: TextStyle(fontSize: 18, color: Colors.grey),
            ),
            SizedBox(height: 8),
            Text(
              'Accept link requests to start chatting',
              style: TextStyle(color: Colors.grey),
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(8),
      itemCount: acceptedLinks.length,
      itemBuilder: (context, index) {
        final link = acceptedLinks[index];
        return Card(
          child: ListTile(
            leading: CircleAvatar(
              child: Icon(Icons.business),
            ),
            title: Text(link.consumerName ?? 'Consumer'),
            subtitle: Text('Tap to open chat'),
            trailing: Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ChatScreen(
                    link: link,
                    currentUser: widget.user,
                  ),
                ),
              );
            },
          ),
        );
      },
    );
  }

  Widget _buildProfileTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        ListTile(title: const Text('Email'), subtitle: Text(widget.user.email)),
        ListTile(title: const Text('Role'), subtitle: Text(widget.user.role)),
        const SizedBox(height: 24),
        ElevatedButton(
          onPressed: _logout,
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.red,
            foregroundColor: Colors.white,
          ),
          child: const Text('Logout'),
        ),
      ],
    );
  }

  void _logout() {
    Navigator.of(context).pushNamedAndRemoveUntil('/', (route) => false);
  }
}
