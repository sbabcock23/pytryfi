import {
  Table,
  Column,
  Model,
  PrimaryKey,
  ForeignKey,
  BelongsTo,
  HasMany,
  Index,
} from "sequelize-typescript";
import { Pet } from "./pet";
import { SleepAmounts } from "./sleep-amount";

@Table({ tableName: "RestSummary" })
export class RestSummary extends Model<RestSummary> {
  @PrimaryKey
  @Column
  id!: string;

  @ForeignKey(() => Pet)
  @Index
  @Column
  pet_id!: string;

  @BelongsTo(() => Pet)
  pet!: Pet;

  @Column
  period_type!: "DAILY" | "WEEKLY" | "MONTHLY";

  @Column
  start_date!: Date;

  @Column
  end_date!: Date;

  @HasMany(() => SleepAmounts)
  sleepAmounts!: SleepAmounts[];
}
