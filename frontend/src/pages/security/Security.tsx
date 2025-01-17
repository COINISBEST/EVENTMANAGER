import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Switch,
  Button,
  Grid,
  LinearProgress,
  Divider,
} from '@mui/material';
import {
  Security as SecurityIcon,
  Phonelink as DeviceIcon,
  VpnKey as KeyIcon,
} from '@mui/icons-material';

const Security: React.FC = () => {
  const [is2FAEnabled, setIs2FAEnabled] = useState(false);
  const [securityScore, setSecurityScore] = useState(70);

  const handleToggle2FA = () => {
    setIs2FAEnabled(!is2FAEnabled);
    // Handle 2FA toggle
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Security Settings
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <SecurityIcon sx={{ mr: 1 }} />
              <Typography variant="h6">Security Overview</Typography>
            </Box>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" gutterBottom>
                Security Score
              </Typography>
              <LinearProgress
                variant="determinate"
                value={securityScore}
                sx={{ height: 8, borderRadius: 4 }}
              />
              <Typography variant="body2" sx={{ mt: 1 }}>
                Your account is {securityScore}% secure
              </Typography>
            </Box>
            <List>
              <ListItem>
                <ListItemText
                  primary="Two-Factor Authentication"
                  secondary="Add an extra layer of security to your account"
                />
                <ListItemSecondaryAction>
                  <Switch
                    edge="end"
                    checked={is2FAEnabled}
                    onChange={handleToggle2FA}
                  />
                </ListItemSecondaryAction>
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText
                  primary="Change Password"
                  secondary="Regularly update your password to keep your account secure"
                />
                <ListItemSecondaryAction>
                  <Button variant="outlined" size="small">
                    Change
                  </Button>
                </ListItemSecondaryAction>
              </ListItem>
            </List>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <DeviceIcon sx={{ mr: 1 }} />
              <Typography variant="h6">Connected Devices</Typography>
            </Box>
            <List>
              {/* Add connected devices list here */}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <KeyIcon sx={{ mr: 1 }} />
              <Typography variant="h6">Recent Activity</Typography>
            </Box>
            <List>
              {/* Add activity list here */}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Security; 