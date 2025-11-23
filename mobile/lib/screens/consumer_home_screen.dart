import 'package:flutter/material.dart';
import '../models/user.dart';
import '../models/link.dart';
import '../models/order.dart';
import '../models/product.dart';
import '../services/link_service.dart';
import '../services/order_service.dart';
import '../services/product_service.dart';
import 'complaints_screen.dart';
import 'chat_screen.dart';

class ConsumerHomeScreen extends StatefulWidget {
  final User user;

  const ConsumerHomeScreen({super.key, required this.user});

  @override
  State<ConsumerHomeScreen> createState() => _ConsumerHomeScreenState();
}

class _ConsumerHomeScreenState extends State<ConsumerHomeScreen> {
  int _selectedIndex = 0;
  final _linkService = LinkService();
  final _orderService = OrderService();
  final _productService = ProductService();

  List<Link> _links = [];
  List<Order> _orders = [];
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
      final links = await _linkService.getMyLinks();
      final orders = await _orderService.getMyOrders();

      // Load products from accepted suppliers
      List<Product> allProducts = [];
      for (var link in links.where((l) => l.status == 'accepted')) {
        try {
          final products = await _productService.getSupplierProducts(
            link.supplierId,
          );
          allProducts.addAll(products);
        } catch (e) {
          print('Error loading products for supplier ${link.supplierId}: $e');
        }
      }

      setState(() {
        _links = links;
        _orders = orders;
        _products = allProducts;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Error loading data: $e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final screens = [
      _buildHomeTab(),
      _buildLinksTab(),
      _buildCatalogTab(),
      _buildOrdersTab(),
      _buildChatsTab(),
      ComplaintsScreen(
        isSupplier: false,
        acceptedLinks: _links.where((link) => link.status == 'accepted').toList(),
      ),
      _buildProfileTab(),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Consumer App'),
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
          NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.link), label: 'Links'),
          NavigationDestination(
            icon: Icon(Icons.shopping_bag),
            label: 'Catalog',
          ),
          NavigationDestination(
            icon: Icon(Icons.shopping_cart),
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
            subtitle: const Text('Consumer Dashboard'),
          ),
        ),
        const SizedBox(height: 16),
        _buildStatCard(
          'Active Links',
          _links.where((l) => l.status == 'accepted').length,
        ),
        _buildStatCard('Total Orders', _orders.length),
        _buildStatCard(
          'Pending Orders',
          _orders.where((o) => o.status == 'pending').length,
        ),
      ],
    );
  }

  Widget _buildStatCard(String title, int count) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: const TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 8),
            Text(
              '$count',
              style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLinksTab() {
    return Stack(
      children: [
        _links.isEmpty
            ? Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.link_off, size: 64, color: Colors.grey),
                    SizedBox(height: 16),
                    Text(
                      'No links yet',
                      style: TextStyle(fontSize: 18, color: Colors.grey),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Tap + to request a connection',
                      style: TextStyle(color: Colors.grey),
                    ),
                  ],
                ),
              )
            : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: _links.length,
                itemBuilder: (context, index) {
                  final link = _links[index];
                  return Card(
                    child: ListTile(
                      title: Text('Link #${link.id}'),
                      subtitle: Text('Status: ${link.status}'),
                      trailing: _buildLinkStatusChip(link.status),
                    ),
                  );
                },
              ),
        Positioned(
          right: 16,
          bottom: 16,
          child: FloatingActionButton(
            onPressed: _showRequestLinkDialog,
            child: Icon(Icons.add),
            tooltip: 'Request Link',
          ),
        ),
      ],
    );
  }

  void _showRequestLinkDialog() {
    final supplierIdController = TextEditingController();
    final notesController = TextEditingController();

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Request Link to Supplier'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: supplierIdController,
              decoration: InputDecoration(
                labelText: 'Supplier ID',
                hintText: 'Enter supplier ID',
              ),
              keyboardType: TextInputType.number,
            ),
            SizedBox(height: 16),
            TextField(
              controller: notesController,
              decoration: InputDecoration(
                labelText: 'Notes (optional)',
                hintText: 'Add a message',
              ),
              maxLines: 3,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              final supplierId = int.tryParse(supplierIdController.text);
              if (supplierId == null) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Please enter a valid supplier ID')),
                );
                return;
              }

              try {
                await _linkService.requestLink(
                  supplierId,
                  notesController.text,
                );
                Navigator.pop(context);
                ScaffoldMessenger.of(
                  context,
                ).showSnackBar(SnackBar(content: Text('Link request sent!')));
                _loadData();
              } catch (e) {
                ScaffoldMessenger.of(
                  context,
                ).showSnackBar(SnackBar(content: Text('Error: $e')));
              }
            },
            child: Text('Send Request'),
          ),
        ],
      ),
    );
  }

  Widget _buildLinkStatusChip(String status) {
    Color color;
    switch (status) {
      case 'accepted':
        color = Colors.green;
        break;
      case 'pending':
        color = Colors.orange;
        break;
      default:
        color = Colors.grey;
    }
    return Chip(label: Text(status), backgroundColor: color.withOpacity(0.2));
  }

  Widget _buildCatalogTab() {
    if (_products.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.shopping_bag_outlined, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text(
              'No products available',
              style: TextStyle(fontSize: 18, color: Colors.grey),
            ),
            SizedBox(height: 8),
            Text(
              'Request a link to suppliers first',
              style: TextStyle(color: Colors.grey),
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _products.length,
      itemBuilder: (context, index) {
        final product = _products[index];
        return Card(
          child: ListTile(
            leading: CircleAvatar(child: Icon(Icons.shopping_bag)),
            title: Text(product.name),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(product.description ?? ''),
                SizedBox(height: 4),
                Text(
                  '\$${product.price} per ${product.unit}',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.green,
                  ),
                ),
                Text('Stock: ${product.stockQuantity}'),
              ],
            ),
            isThreeLine: true,
            trailing: IconButton(
              icon: Icon(Icons.add_shopping_cart, color: Colors.blue),
              onPressed: () => _showOrderDialog(product),
            ),
          ),
        );
      },
    );
  }

  void _showOrderDialog(Product product) {
    final quantityController = TextEditingController(text: '1');

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Order ${product.name}'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Price: \$${product.price} per ${product.unit}'),
            SizedBox(height: 16),
            TextField(
              controller: quantityController,
              decoration: InputDecoration(
                labelText: 'Quantity',
                suffixText: product.unit,
              ),
              keyboardType: TextInputType.number,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              final quantity = int.tryParse(quantityController.text);
              if (quantity == null || quantity <= 0) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Please enter a valid quantity')),
                );
                return;
              }

              if (quantity > product.stockQuantity) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Not enough stock available')),
                );
                return;
              }

              try {
                final orderRequest = CreateOrderRequest(
                  supplierId: product.supplierId,
                  items: [
                    OrderItemRequest(productId: product.id, quantity: quantity),
                  ],
                );

                await _orderService.createOrder(orderRequest);
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Order created successfully!')),
                );
                _loadData();
              } catch (e) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Error creating order: $e')),
                );
              }
            },
            child: Text('Create Order'),
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
            trailing: Text(order.status),
          ),
        );
      },
    );
  }

  Widget _buildChatsTab() {
    // Filter only accepted links for chat
    final acceptedLinks = _links.where((link) => link.status == 'accepted').toList();
    
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
              'Connect with suppliers to start chatting',
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
              child: Icon(Icons.store),
            ),
            title: Text(link.supplierName ?? 'Supplier'),
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
        ListTile(
          title: const Text('Phone'),
          subtitle: Text(widget.user.phone ?? 'N/A'),
        ),
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
