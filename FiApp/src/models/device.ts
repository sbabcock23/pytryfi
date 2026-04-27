import {
  Table,
  Column,
  Model,
  PrimaryKey,
  ForeignKey,
  BelongsTo,
  Index,
} from "sequelize-typescript";
import { Pet } from "./pet";

@Table({ tableName: "Devices" })
export class Device extends Model<Device> {
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
  module_id!: string;

  @Column
  battery_percent?: number;

  @Column
  uptime?: number;

  @Column
  subscription_id?: string;

  @Column
  has_active_subscription!: boolean;

  @Column
  next_location_update_expected_by?: Date;
}
