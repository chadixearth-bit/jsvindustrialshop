// Function to fetch and display delivery details
async function fetchDeliveryDetails(deliveryId) {
    console.log('Fetching delivery details for ID:', deliveryId);
    try {
        const response = await fetch(`/requisition/delivery/details/${deliveryId}/`);
        if (!response.ok) {
            throw new Error('Failed to fetch delivery details');
        }
        const data = await response.json();
        console.log('Received delivery data:', data);
        showDeliveryModal(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load delivery details. Please try again.');
    }
}

// Function to show the delivery modal
function showDeliveryModal(deliveryData) {
    console.log('Showing modal with data:', deliveryData);
    const modal = document.getElementById('deliveryModal');
    if (!modal) {
        console.error('Modal element not found');
        return;
    }

    // Update modal content with delivery data
    document.getElementById('deliveryId').textContent = deliveryData.id;
    document.getElementById('sourceWarehouse').textContent = deliveryData.source_warehouse;
    document.getElementById('destWarehouse').textContent = deliveryData.destination_warehouse;
    document.getElementById('deliveryStatus').textContent = deliveryData.status;
    document.getElementById('createdDate').textContent = deliveryData.created_at;
    document.getElementById('estimatedDate').textContent = deliveryData.estimated_delivery_date || 'Not specified';

    // Clear and populate items table
    const tableBody = document.getElementById('itemsTableBody');
    if (!tableBody) {
        console.error('Table body element not found');
        return;
    }

    tableBody.innerHTML = '';
    deliveryData.items.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${item.item_name}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${item.brand}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${item.category}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${item.quantity}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${item.unit}</td>
        `;
        tableBody.appendChild(row);
    });

    // Show modal
    modal.classList.remove('hidden');
}

// Function to close the delivery modal
function closeDeliveryModal() {
    console.log('Closing modal');
    const modal = document.getElementById('deliveryModal');
    if (modal) {
        modal.classList.add('hidden');
    } else {
        console.error('Modal element not found');
    }
}

// Close modal when clicking outside
document.addEventListener('DOMContentLoaded', function() {
    console.log('Setting up event listeners');
    const modal = document.getElementById('deliveryModal');
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                closeDeliveryModal();
            }
        });

        // Close modal on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeDeliveryModal();
            }
        });
    } else {
        console.error('Modal element not found during initialization');
    }
});
