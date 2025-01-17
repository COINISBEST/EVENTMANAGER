import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Switch,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';

interface Game {
  id: number;
  name: string;
  price: number;
  available: boolean;
  maxPlayers: number;
  duration: number; // in minutes
}

const GameStallDashboard: React.FC = () => {
  const [games, setGames] = useState<Game[]>([
    {
      id: 1,
      name: 'Laser Tag',
      price: 15.99,
      available: true,
      maxPlayers: 8,
      duration: 30,
    },
    // Add more games
  ]);

  const handleAvailabilityChange = (id: number) => {
    setGames(games.map(game => 
      game.id === id ? { ...game, available: !game.available } : game
    ));
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Game Stall Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {/* Handle add game */}}
        >
          Add Game
        </Button>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Games List
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>Price</TableCell>
                    <TableCell>Max Players</TableCell>
                    <TableCell>Duration</TableCell>
                    <TableCell>Available</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {games.map((game) => (
                    <TableRow key={game.id}>
                      <TableCell>{game.name}</TableCell>
                      <TableCell>${game.price}</TableCell>
                      <TableCell>{game.maxPlayers}</TableCell>
                      <TableCell>{game.duration} min</TableCell>
                      <TableCell>
                        <Switch
                          checked={game.available}
                          onChange={() => handleAvailabilityChange(game.id)}
                        />
                      </TableCell>
                      <TableCell>
                        <IconButton size="small">
                          <EditIcon />
                        </IconButton>
                        <IconButton size="small" color="error">
                          <DeleteIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Current Sessions
            </Typography>
            {/* Add active game sessions here */}
          </Paper>
          <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              Today's Revenue
            </Typography>
            {/* Add revenue stats here */}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default GameStallDashboard; 