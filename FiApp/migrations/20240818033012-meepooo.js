"use strict";

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.changeColumn("ActivitySummary", "id", {
      type: Sequelize.UUID,
      allowNull: false,
      defaultValue: Sequelize.literal("uuid_generate_v4()"),
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.changeColumn("ActivitySummary", "id", {
      type: Sequelize.UUID,
      allowNull: false,
      defaultValue: null,
    });
  },
};
