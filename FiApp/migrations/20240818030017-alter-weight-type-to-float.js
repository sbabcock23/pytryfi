"use strict";

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.changeColumn("Pets", "weight", {
      type: Sequelize.FLOAT,
      allowNull: false,
    });
  },

  down: async (queryInterface, Sequelize) => {
    // If you want to revert this migration, you can change the column type back to INTEGER or the previous type
    await queryInterface.changeColumn("Pets", "weight", {
      type: Sequelize.INTEGER,
      allowNull: false,
    });
  },
};
