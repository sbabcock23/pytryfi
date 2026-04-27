import {
  Table,
  Column,
  Model,
  PrimaryKey,
  ForeignKey,
  BelongsTo,
  Index,
  DataType,
  Default,
} from "sequelize-typescript";
import { ActivitySummary } from "./activity-summary";

@Table({ tableName: "DailySteps" })
export class DailySteps extends Model<DailySteps> {
  @PrimaryKey
  @Default(DataType.UUIDV4)
  @Column({
    type: DataType.UUID,
    allowNull: false,
  })
  id!: string;

  @ForeignKey(() => ActivitySummary)
  @Index
  @Column({
    type: DataType.UUID,
    allowNull: false,
  })
  activity_summary_id!: string;

  @BelongsTo(() => ActivitySummary)
  activitySummary!: ActivitySummary;

  @Column({
    type: DataType.DATE,
    allowNull: false,
  })
  date!: Date;

  @Column({
    type: DataType.INTEGER,
    allowNull: false,
  })
  total_steps!: number;

  @Column({
    type: DataType.INTEGER,
    allowNull: false,
  })
  step_goal!: number;
}
