// ignore_for_file: non_constant_identifier_names

import 'dart:convert';
import "package:http/http.dart" as http;

import 'package:gym_rs/models/exerciseProgram.dart';

class Api {
  static Future<List<ExerciseProgram>> PostData(List<int> array) async {
    var uri = Uri.parse('https://api-gymrs.onrender.com/PostData');
    var headers = {'Content-Type': 'application/json'};
    var body = json.encode({"array": array});
    var response = await http.post(uri, headers: headers, body: body);
    final jsonData = json.decode(response.body);
    List<ExerciseProgram> exercises = List.generate(
      jsonData.length,
      (index) => ExerciseProgram.fromJson(jsonData[index]),
    );
    return exercises;
  }
}
