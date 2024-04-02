import { Box } from "@mui/material";
import PredictionsGraph from "./PredictionsGraph";


const Predictions = () => {
    return(
        <div className="Predictions">
            <Box
      width="100%"
      height="100%"
      display="grid"
      gap="1.5rem"
    >
        <PredictionsGraph />
    </Box>
        </div>
    )
}

export default Predictions;