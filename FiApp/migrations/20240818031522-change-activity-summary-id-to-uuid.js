"use strict";

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.sequelize.query(
      'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',
    );
  },

  down: async (queryInterface, Sequelize) => {
    // Leave uuid-ossp installed; other local schema objects may rely on it.
  },
};
