import React, { useState } from 'react';
import { Button, TextField, Grid } from "@mui/material";

const BuySellComponent = () => {
  const [amount, setAmount] = useState('');
  // const [action, setAction] = useState('');

  const handleBuy = () => {
    // Implement buy functionality here
    console.log('Buying', amount, 'BTC');
  };

  const handleSell = () => {
    // Implement sell functionality here
    console.log('Selling', amount, 'BTC');
  };

  return (
    <Grid container spacing={2} alignItems="center">
      <Grid item>
        <TextField
          type="number"
          label="Amount"
          variant="outlined"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
      </Grid>
      <Grid item>
        <Button variant="contained" color="primary" onClick={handleBuy}>
          Buy
        </Button>
      </Grid>
      <Grid item>
        <Button variant="contained" color="secondary" onClick={handleSell}>
          Sell
        </Button>
      </Grid>
    </Grid>
  );
};

export default BuySellComponent;
