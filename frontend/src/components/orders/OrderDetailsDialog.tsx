import React from 'react';
import {
  Dialog,
  DialogContent,
} from '@mui/material';
import { Order, OrderStatus } from '../../api/types';
import OrderDetails from './OrderDetails';

interface OrderDetailsDialogProps {
  open: boolean;
  order: Order | null;
  onClose: () => void;
  onUpdateStatus?: (orderId: number, status: OrderStatus) => Promise<void>;
}

const OrderDetailsDialog: React.FC<OrderDetailsDialogProps> = ({
  open,
  order,
  onClose,
  onUpdateStatus,
}) => {
  const handleUpdateStatus = async (status: OrderStatus) => {
    if (order && onUpdateStatus) {
      await onUpdateStatus(order.id, status);
    }
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
    >
      <DialogContent>
        {order && (
          <OrderDetails
            order={order}
            onUpdateStatus={onUpdateStatus ? handleUpdateStatus : undefined}
            onClose={onClose}
          />
        )}
      </DialogContent>
    </Dialog>
  );
};

export default OrderDetailsDialog; 