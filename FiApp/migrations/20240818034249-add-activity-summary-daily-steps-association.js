"use strict";

module.exports = {
  up: async (queryInterface, Sequelize) => {
    const tableDefinition = await queryInterface.describeTable("DailySteps");

    if (!tableDefinition.activity_summary_id) {
      await queryInterface.addColumn("DailySteps", "activity_summary_id", {
        type: Sequelize.UUID,
        allowNull: false,
        references: {
          model: "ActivitySummary",
          key: "id",
        },
        onUpdate: "CASCADE",
        onDelete: "CASCADE",
      });

      await queryInterface.addIndex("DailySteps", ["activity_summary_id"], {
        name: "daily_steps_activity_summary_id",
      });
    }
  },

  down: async (queryInterface, Sequelize) => {
    const tableDefinition = await queryInterface.describeTable("DailySteps");

    if (tableDefinition.activity_summary_id) {
      await queryInterface.removeIndex(
        "DailySteps",
        "daily_steps_activity_summary_id",
      );
      await queryInterface.removeColumn("DailySteps", "activity_summary_id");
    }
  },
};
