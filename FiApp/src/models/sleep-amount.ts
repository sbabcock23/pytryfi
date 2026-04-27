import {
  Table,
  Column,
  Model,
  PrimaryKey,
  ForeignKey,
  BelongsTo,
  Index,
} from "sequelize-typescript";
import { RestSummary } from "./rest-summary";

@Table({ tableName: "SleepAmounts" })
export class SleepAmounts extends Model<SleepAmounts> {
  @PrimaryKey
  @Column
  id!: string;

  @ForeignKey(() => RestSummary)
  @Index
  @Column
  rest_summary_id!: string;

  @BelongsTo(() => RestSummary)
  restSummary!: RestSummary;

  @Column
  type!: "SLEEP" | "NAP";

  @Column
  duration!: number;
}
