import 'package:flutter/material.dart';
import '../models/complaint.dart';
import '../models/link.dart';
import '../services/complaint_service.dart';

class ComplaintsScreen extends StatefulWidget {
  final bool isSupplier;
  final List<Link> acceptedLinks;

  const ComplaintsScreen({
    super.key,
    required this.isSupplier,
    this.acceptedLinks = const [],
  });

  @override
  State<ComplaintsScreen> createState() => _ComplaintsScreenState();
}

class _ComplaintsScreenState extends State<ComplaintsScreen> {
  final ComplaintService _complaintService = ComplaintService();
  List<Complaint> _complaints = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadComplaints();
  }

  Future<void> _loadComplaints() async {
    setState(() => _isLoading = true);
    try {
      final complaints = widget.isSupplier
          ? await _complaintService.getOpenComplaints()
          : await _complaintService.getMyComplaints();
      setState(() {
        _complaints = complaints;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading complaints: $e')),
        );
      }
    }
  }

  Future<void> _showCreateComplaintDialog() async {
    if (widget.acceptedLinks.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('You need to have accepted links to create complaints'),
        ),
      );
      return;
    }

    final titleController = TextEditingController();
    final descriptionController = TextEditingController();
    String selectedType = 'product_quality';
    Link? selectedLink = widget.acceptedLinks.first;

    await showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Create Complaint'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: titleController,
                decoration: const InputDecoration(
                  labelText: 'Title',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: descriptionController,
                decoration: const InputDecoration(
                  labelText: 'Description',
                  border: OutlineInputBorder(),
                ),
                maxLines: 3,
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<Link>(
                value: selectedLink,
                decoration: const InputDecoration(
                  labelText: 'Supplier',
                  border: OutlineInputBorder(),
                ),
                items: widget.acceptedLinks.map((link) {
                  return DropdownMenuItem<Link>(
                    value: link,
                    child: Text(link.supplierName ?? 'Supplier ${link.supplierId}'),
                  );
                }).toList(),
                onChanged: (value) {
                  selectedLink = value;
                },
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                value: selectedType,
                decoration: const InputDecoration(
                  labelText: 'Type',
                  border: OutlineInputBorder(),
                ),
                items: const [
                  DropdownMenuItem(
                    value: 'product_quality',
                    child: Text('Product Quality'),
                  ),
                  DropdownMenuItem(
                    value: 'delivery',
                    child: Text('Delivery'),
                  ),
                  DropdownMenuItem(
                    value: 'service',
                    child: Text('Service'),
                  ),
                  DropdownMenuItem(
                    value: 'other',
                    child: Text('Other'),
                  ),
                ],
                onChanged: (value) {
                  selectedType = value ?? 'product_quality';
                },
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              if (titleController.text.isNotEmpty &&
                  descriptionController.text.isNotEmpty) {
                try {
                  if (selectedLink == null) {
                    throw Exception('Please select a supplier');
                  }
                  await _complaintService.createComplaint(
                    CreateComplaintRequest(
                      linkId: selectedLink!.id,
                      title: titleController.text,
                      description: descriptionController.text,
                      complaintType: selectedType,
                    ),
                  );
                  if (mounted) {
                    Navigator.pop(context);
                    _loadComplaints();
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Complaint created successfully'),
                      ),
                    );
                  }
                } catch (e) {
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Error creating complaint: $e')),
                    );
                  }
                }
              }
            },
            child: const Text('Create'),
          ),
        ],
      ),
    );
  }

  Future<void> _showComplaintDetails(Complaint complaint) async {
    await showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(complaint.title),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              _buildInfoRow('Type', _formatType(complaint.complaintType)),
              _buildInfoRow('Status', _formatStatus(complaint.status)),
              _buildInfoRow('Priority', complaint.priority),
              _buildInfoRow('Created', _formatDate(complaint.createdAt)),
              const SizedBox(height: 16),
              const Text(
                'Description:',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Text(complaint.description),
              if (complaint.resolutionNotes != null) ...[
                const SizedBox(height: 16),
                const Text(
                  'Resolution Notes:',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Text(complaint.resolutionNotes!),
              ],
            ],
          ),
        ),
        actions: [
          if (widget.isSupplier && complaint.status == 'open')
            TextButton(
              onPressed: () async {
                try {
                  await _complaintService.updateComplaint(
                    complaint.id,
                    status: 'in_progress',
                  );
                  if (mounted) {
                    Navigator.pop(context);
                    _loadComplaints();
                  }
                } catch (e) {
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Error updating complaint: $e')),
                    );
                  }
                }
              },
              child: const Text('Start Working'),
            ),
          if (widget.isSupplier && complaint.status == 'in_progress')
            TextButton(
              onPressed: () async {
                final notesController = TextEditingController();
                await showDialog(
                  context: context,
                  builder: (ctx) => AlertDialog(
                    title: const Text('Resolve Complaint'),
                    content: TextField(
                      controller: notesController,
                      decoration: const InputDecoration(
                        labelText: 'Resolution Notes',
                        border: OutlineInputBorder(),
                      ),
                      maxLines: 3,
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(ctx),
                        child: const Text('Cancel'),
                      ),
                      ElevatedButton(
                        onPressed: () async {
                          try {
                            await _complaintService.updateComplaint(
                              complaint.id,
                              status: 'resolved',
                              resolutionNotes: notesController.text,
                            );
                            if (mounted) {
                              Navigator.pop(ctx);
                              Navigator.pop(context);
                              _loadComplaints();
                            }
                          } catch (e) {
                            if (mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(
                                  content: Text('Error resolving complaint: $e'),
                                ),
                              );
                            }
                          }
                        },
                        child: const Text('Resolve'),
                      ),
                    ],
                  ),
                );
              },
              child: const Text('Resolve'),
            ),
          if (!widget.isSupplier &&
              complaint.status == 'in_progress' &&
              complaint.priority != 'high')
            TextButton(
              onPressed: () async {
                try {
                  await _complaintService.escalateComplaint(complaint.id);
                  if (mounted) {
                    Navigator.pop(context);
                    _loadComplaints();
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Complaint escalated to high priority'),
                      ),
                    );
                  }
                } catch (e) {
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Error escalating complaint: $e')),
                    );
                  }
                }
              },
              child: const Text('Escalate'),
            ),
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 80,
            child: Text(
              '$label:',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }

  String _formatType(String type) {
    switch (type) {
      case 'product_quality':
        return 'Product Quality';
      case 'delivery':
        return 'Delivery';
      case 'service':
        return 'Service';
      default:
        return 'Other';
    }
  }

  String _formatStatus(String status) {
    switch (status) {
      case 'open':
        return 'Open';
      case 'in_progress':
        return 'In Progress';
      case 'resolved':
        return 'Resolved';
      case 'rejected':
        return 'Rejected';
      default:
        return status;
    }
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'open':
        return Colors.orange;
      case 'in_progress':
        return Colors.blue;
      case 'resolved':
        return Colors.green;
      case 'rejected':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year}';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Complaints'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadComplaints,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _complaints.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(
                        Icons.report_problem,
                        size: 64,
                        color: Colors.grey,
                      ),
                      const SizedBox(height: 16),
                      const Text(
                        'No complaints found',
                        style: TextStyle(
                          fontSize: 18,
                          color: Colors.grey,
                        ),
                      ),
                    ],
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(8),
                  itemCount: _complaints.length,
                  itemBuilder: (context, index) {
                    final complaint = _complaints[index];
                    return Card(
                      margin: const EdgeInsets.symmetric(vertical: 4),
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: _getStatusColor(complaint.status),
                          child: Icon(
                            _getComplaintIcon(complaint.complaintType),
                            color: Colors.white,
                          ),
                        ),
                        title: Text(complaint.title),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Status: ${_formatStatus(complaint.status)}',
                            ),
                            Text(
                              'Priority: ${complaint.priority}',
                              style: TextStyle(
                                color: complaint.priority == 'high'
                                    ? Colors.red
                                    : complaint.priority == 'medium'
                                        ? Colors.orange
                                        : Colors.grey,
                              ),
                            ),
                          ],
                        ),
                        trailing: Icon(
                          Icons.arrow_forward_ios,
                          size: 16,
                        ),
                        onTap: () => _showComplaintDetails(complaint),
                      ),
                    );
                  },
                ),
      floatingActionButton: !widget.isSupplier
          ? FloatingActionButton(
              onPressed: _showCreateComplaintDialog,
              child: const Icon(Icons.add),
            )
          : null,
    );
  }

  IconData _getComplaintIcon(String type) {
    switch (type) {
      case 'product_quality':
        return Icons.inventory;
      case 'delivery':
        return Icons.local_shipping;
      case 'service':
        return Icons.support_agent;
      default:
        return Icons.report;
    }
  }
}
