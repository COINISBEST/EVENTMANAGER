import React, { useState, ChangeEvent } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Button,
  TextField,
  IconButton,
  Divider,
} from '@mui/material';
import {
  Add as AddIcon,
  Remove as RemoveIcon,
} from '@mui/icons-material';
import { MenuItem } from '../../api/types';
import { useNavigate } from 'react-router-dom';

interface CartItem extends MenuItem {
  quantity: number;
}

interface CreateOrderProps {
  stallId: number;
  menuItems: MenuItem[];
  onSubmit: (items: { item_id: number; quantity: number }[]) => Promise<void>;
}

const CreateOrder: React.FC<CreateOrderProps> = ({
  stallId,
  menuItems,
  onSubmit,
}) => {
  const navigate = useNavigate();
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleAddToCart = (item: MenuItem): void => {
    const existingItem = cartItems.find((cartItem: CartItem) => cartItem.id === item.id);
    if (existingItem) {
      setCartItems(
        cartItems.map((cartItem: CartItem) =>
          cartItem.id === item.id
            ? { ...cartItem, quantity: cartItem.quantity + 1 }
            : cartItem
        )
      );
    } else {
      setCartItems([...cartItems, { ...item, quantity: 1 }]);
    }
  };

  const handleUpdateQuantity = (itemId: number, newQuantity: number): void => {
    if (newQuantity === 0) {
      setCartItems(cartItems.filter((item: CartItem) => item.id !== itemId));
    } else {
      setCartItems(
        cartItems.map((item: CartItem) =>
          item.id === itemId ? { ...item, quantity: newQuantity } : item
        )
      );
    }
  };

  const calculateTotal = (): number => {
    return cartItems.reduce(
      (total: number, item: CartItem) => total + item.price * item.quantity,
      0
    );
  };

  const handleSubmit = async (): Promise<void> => {
    setIsSubmitting(true);
    try {
      await onSubmit(
        cartItems.map((item: CartItem) => ({
          item_id: item.id,
          quantity: item.quantity,
        }))
      );
      navigate('/orders');
    } catch (error) {
      console.error('Failed to create order:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Create Order
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Typography variant="h6" gutterBottom>
            Menu Items
          </Typography>
          <Grid container spacing={2}>
            {menuItems.map((item) => (
              <Grid item xs={12} sm={6} key={item.id}>
                <Card>
                  {item.image_url && (
                    <CardMedia
                      component="img"
                      height="140"
                      image={item.image_url}
                      alt={item.name}
                    />
                  )}
                  <CardContent>
                    <Typography variant="h6">{item.name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {item.description}
                    </Typography>
                    <Box
                      sx={{
                        mt: 2,
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                      }}
                    >
                      <Typography variant="h6">${item.price.toFixed(2)}</Typography>
                      <Button
                        variant="contained"
                        size="small"
                        onClick={() => handleAddToCart(item)}
                        disabled={!item.is_available}
                      >
                        Add to Cart
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Cart
            </Typography>
            {cartItems.length === 0 ? (
              <Typography color="text.secondary">Your cart is empty</Typography>
            ) : (
              <>
                {cartItems.map((item) => (
                  <Box key={item.id} sx={{ mb: 2 }}>
                    <Box
                      sx={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                      }}
                    >
                      <Typography>{item.name}</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <IconButton
                          size="small"
                          onClick={() =>
                            handleUpdateQuantity(item.id, item.quantity - 1)
                          }
                        >
                          <RemoveIcon />
                        </IconButton>
                        <TextField
                          size="small"
                          value={item.quantity}
                          onChange={(e) =>
                            handleUpdateQuantity(
                              item.id,
                              parseInt(e.target.value) || 0
                            )
                          }
                          sx={{ width: 60, mx: 1 }}
                        />
                        <IconButton
                          size="small"
                          onClick={() =>
                            handleUpdateQuantity(item.id, item.quantity + 1)
                          }
                        >
                          <AddIcon />
                        </IconButton>
                      </Box>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      ${(item.price * item.quantity).toFixed(2)}
                    </Typography>
                  </Box>
                ))}
                <Divider sx={{ my: 2 }} />
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    mb: 2,
                  }}
                >
                  <Typography variant="h6">Total:</Typography>
                  <Typography variant="h6">
                    ${calculateTotal().toFixed(2)}
                  </Typography>
                </Box>
                <Button
                  fullWidth
                  variant="contained"
                  onClick={handleSubmit}
                  disabled={cartItems.length === 0 || isSubmitting}
                >
                  Place Order
                </Button>
              </>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CreateOrder; 