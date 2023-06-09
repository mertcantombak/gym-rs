// ignore_for_file: non_constant_identifier_names, file_names

class ExerciseProgram {
  int? level_0;
  String? Title;
  String? Desc;
  String? Type;
  String? BodyPart;
  String? Equipment;
  String? Level;
  double? Rating;
  String? RatingDesc;
  ExerciseProgram(this.level_0, this.Title, this.Desc, this.Type, this.BodyPart,
      this.Equipment, this.Level, this.Rating, this.RatingDesc);
  ExerciseProgram.fromJson(Map json) {
    level_0 = json["level_0"] ?? -1;
    Title = json["Title"] ?? "";
    Desc = json["Desc"] ?? "";
    Type = json["Type"] ?? "";
    BodyPart = json["BodyPart"] ?? "";
    Equipment = json["Equipment"] ?? "";
    Level = json["Level"] ?? "";
    Rating = json["Rating"] ?? 0;
    RatingDesc = json["RatingDesc"] ?? "";
  }
  Map toJson() {
    return {
      "level_0": level_0,
      "Title": Title,
      "Desc": Desc,
      "Type": Type,
      "BodyPart": BodyPart,
      "Equipment": Equipment,
      "Level": Level,
      "Rating": Rating,
      "RatingDesc": RatingDesc,
    };
  }
}
