import {
  Table,
  Column,
  Model,
  PrimaryKey,
  ForeignKey,
  BelongsTo,
  HasMany,
  Index,
  DataType,
  Default,
  AfterCreate,
} from "sequelize-typescript";
import { Pet } from "./pet";
import { DailySteps } from "./daily-steps";
import { v4 as uuidv4 } from "uuid";

@Table({ tableName: "ActivitySummary" })
export class ActivitySummary extends Model<ActivitySummary> {
  @PrimaryKey
  @Default(uuidv4)
  @Column({ type: DataType.UUID })
  id!: string;

  @ForeignKey(() => Pet)
  @Index
  @Column({
    allowNull: false,
  })
  pet_id!: string;

  @BelongsTo(() => Pet)
  pet!: Pet;

  @Index
  @Column
  period_type!: "DAILY" | "WEEKLY" | "MONTHLY";

  @Column
  start_date!: Date;

  @Column
  end_date!: Date;

  @Column
  total_steps!: number;

  @Column
  step_goal!: number;

  @Column({
    type: DataType.FLOAT,
    allowNull: false,
  })
  total_distance!: number;

  @HasMany(() => DailySteps)
  dailySteps!: DailySteps[];
}
