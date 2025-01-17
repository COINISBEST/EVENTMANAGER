import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Button,
  TablePagination,
} from '@mui/material';
import {
  Visibility as ViewIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';
import { getOrders, cancelOrder } from '../../api/orders';
import { Order, OrderStatus } from '../../api/types';
import { format } from 'date-fns';
import Loading from '../common/Loading';

const OrdersList: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    fetchOrders();
  }, [page, rowsPerPage]);

  const fetchOrders = async () => {
    try {
      const data = await getOrders({
        skip: page * rowsPerPage,
        limit: rowsPerPage,
      });
      setOrders(data);
      // Assuming the total count comes from the backend
      // setTotalCount(totalCount);
    } catch (error) {
      console.error('Failed to fetch orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelOrder = async (orderId: number) => {
    try {
      await cancelOrder(orderId);
      fetchOrders();
    } catch (error) {
      console.error('Failed to cancel order:', error);
    }
  };

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

  if (loading) {
    return <Loading />;
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Orders</Typography>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Order ID</TableCell>
              <TableCell>Date</TableCell>
              <TableCell>Status</TableCell>
              <TableCell align="right">Total Amount</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {orders.map((order) => (
              <TableRow key={order.id}>
                <TableCell>#{order.id}</TableCell>
                <TableCell>
                  {format(new Date(order.created_at), 'PPp')}
                </TableCell>
                <TableCell>
                  <Chip
                    label={order.status}
                    color={getStatusColor(order.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell align="right">
                  ${order.total_amount.toFixed(2)}
                </TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => {/* Handle view order */}}
                  >
                    <ViewIcon />
                  </IconButton>
                  {order.status === OrderStatus.PENDING && (
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => handleCancelOrder(order.id)}
                    >
                      <CancelIcon />
                    </IconButton>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <TablePagination
          component="div"
          count={totalCount}
          page={page}
          onPageChange={(_, newPage) => setPage(newPage)}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={(event) => {
            setRowsPerPage(parseInt(event.target.value, 10));
            setPage(0);
          }}
        />
      </TableContainer>
    </Box>
  );
};

export default OrdersList; 