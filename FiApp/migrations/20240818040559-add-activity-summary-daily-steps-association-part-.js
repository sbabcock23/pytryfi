"use strict";

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addConstraint("ActivitySummary", {
      fields: ["start_date", "end_date", "period_type"],
      type: "unique",
      name: "unique_activity_summary_constraint", // optional: name of the constraint
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.removeConstraint(
      "ActivitySummary",
      "unique_activity_summary_constraint",
    );
  },
};
