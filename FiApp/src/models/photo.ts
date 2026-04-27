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

@Table({ tableName: "Photos" })
export class Photo extends Model<Photo> {
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
  caption?: string;

  @Index
  @Column
  date!: Date;

  @Column
  like_count!: number;

  @Column
  liked!: boolean;

  @Column
  image_url!: string;
}
