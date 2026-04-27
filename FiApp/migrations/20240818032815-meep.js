"use strict";

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.changeColumn("ActivitySummary", "total_distance", {
      type: Sequelize.FLOAT,
      allowNull: false,
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.changeColumn("ActivitySummary", "total_distance", {
      type: Sequelize.INTEGER,
      allowNull: false,
    });
  },
};
