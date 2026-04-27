import {
  Table,
  Column,
  Model,
  PrimaryKey,
  HasMany,
  Index,
} from "sequelize-typescript";
import { Pet } from "./pet";

@Table({ tableName: "Breeds" })
export class Breed extends Model<Breed> {
  @PrimaryKey
  @Column
  id!: string;

  @Index
  @Column
  name!: string;

  @Column
  popularity_score!: number;

  @HasMany(() => Pet)
  pets!: Pet[];
}
