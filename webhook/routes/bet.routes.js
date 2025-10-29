const express = require('express');
const authMiddleware = require('../middlewares/authMiddleware');
const betController = require('../controller/bet.controller');
const roletaController = require('../controller/roleta.controller');
const router = express.Router();


router.post("/apostar/roleta",authMiddleware,betController.novaAposta,roletaController.novaRoletaBet);
/*BetController:


*/

//router.put("/apostar/roleta",authMiddleware);

//router.post("/apostar/mines",authMiddleware);
//router.post("/apostar/777_classic",authMiddleware);

module.exports = router;