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
} from "sequelize-typescript";
import { User } from "./user";
import { Breed } from "./breed";
import { Photo } from "./photo";
import { Device } from "./device";
import { ActivitySummary } from "./activity-summary";
import { RestSummary } from "./rest-summary";

@Table({ tableName: "Pets" })
export class Pet extends Model<Pet> {
  @PrimaryKey
  @Column
  id!: string;

  @Index
  @Column
  name!: string;

  @Column
  home_city_state?: string;

  @Index
  @Column
  year_of_birth!: number;

  @Column
  month_of_birth!: number;

  @Column
  day_of_birth!: number;

  @Index
  @Column
  gender!: "MALE" | "FEMALE";

  @Column({type: DataType.FLOAT})
  weight!: number;

  @Column
  is_purebred!: boolean;

  @ForeignKey(() => Breed)
  @Column
  breed_id!: string;

  @BelongsTo(() => Breed)
  breed!: Breed;

  @Index
  @Column
  instagram_handle?: string;

  @Index
  @Column
  chip?: string;

  @ForeignKey(() => User)
  @Column
  user_id!: string;

  @BelongsTo(() => User)
  user!: User;

  @HasMany(() => Photo)
  photos!: Photo[];

  @HasMany(() => Device)
  devices!: Device[];

  @HasMany(() => ActivitySummary)
  activitySummaries!: ActivitySummary[];

  @HasMany(() => RestSummary)
  restSummaries!: RestSummary[];
}
