import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  Divider,
} from '@mui/material';
import { Order, OrderStatus } from '../../api/types';
import { format } from 'date-fns';

interface OrderDetailsProps {
  order: Order;
  onUpdateStatus?: (status: OrderStatus) => void;
  onClose: () => void;
}

const OrderDetails: React.FC<OrderDetailsProps> = ({
  order,
  onUpdateStatus,
  onClose,
}) => {
  const getStatusColor = (status: OrderStatus) => {
    switch (status) {
      case OrderStatus.PENDING:
        return 'warning';
      case OrderStatus.PREPARING:
        return 'info';
      case OrderStatus.READY:
        return 'success';
      case OrderStatus.COMPLETED:
        return 'default';
      case OrderStatus.CANCELLED:
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h5">Order #{order.id}</Typography>
        <Chip
          label={order.status}
          color={getStatusColor(order.status)}
        />
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Typography variant="subtitle2" color="text.secondary">
            Order Date
          </Typography>
          <Typography variant="body1">
            {format(new Date(order.created_at), 'PPp')}
          </Typography>
        </Grid>
        <Grid item xs={12} md={6}>
          <Typography variant="subtitle2" color="text.secondary">
            Total Amount
          </Typography>
          <Typography variant="body1">
            ${order.total_amount.toFixed(2)}
          </Typography>
        </Grid>
      </Grid>

      <Divider sx={{ my: 3 }} />

      <Typography variant="h6" gutterBottom>
        Order Items
      </Typography>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Item</TableCell>
              <TableCell align="right">Quantity</TableCell>
              <TableCell align="right">Price</TableCell>
              <TableCell align="right">Subtotal</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {order.items.map((item) => (
              <TableRow key={item.id}>
                <TableCell>{item.name}</TableCell>
                <TableCell align="right">{item.quantity}</TableCell>
                <TableCell align="right">${item.price.toFixed(2)}</TableCell>
                <TableCell align="right">${item.subtotal.toFixed(2)}</TableCell>
              </TableRow>
            ))}
            <TableRow>
              <TableCell colSpan={3} align="right">
                <Typography variant="subtitle1">Total</Typography>
              </TableCell>
              <TableCell align="right">
                <Typography variant="subtitle1">
                  ${order.total_amount.toFixed(2)}
                </Typography>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      {onUpdateStatus && order.status !== OrderStatus.COMPLETED && order.status !== OrderStatus.CANCELLED && (
        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          {order.status === OrderStatus.PENDING && (
            <Button
              variant="contained"
              color="primary"
              onClick={() => onUpdateStatus(OrderStatus.PREPARING)}
            >
              Start Preparing
            </Button>
          )}
          {order.status === OrderStatus.PREPARING && (
            <Button
              variant="contained"
              color="success"
              onClick={() => onUpdateStatus(OrderStatus.READY)}
            >
              Mark as Ready
            </Button>
          )}
          {order.status === OrderStatus.READY && (
            <Button
              variant="contained"
              color="success"
              onClick={() => onUpdateStatus(OrderStatus.COMPLETED)}
            >
              Complete Order
            </Button>
          )}
        </Box>
      )}

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button onClick={onClose}>Close</Button>
      </Box>
    </Paper>
  );
};

export default OrderDetails; 