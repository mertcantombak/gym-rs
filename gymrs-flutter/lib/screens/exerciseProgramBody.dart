// ignore_for_file: file_names, unused_local_variable

import 'package:expandable_text/expandable_text.dart';
import 'package:flutter/material.dart';
import 'package:gym_rs/models/exerciseProgram.dart';

class ExerciseProgramBodyScreen extends StatefulWidget {
  final List<ExerciseProgram> exerciseList;
  const ExerciseProgramBodyScreen({super.key, required this.exerciseList});

  @override
  State<ExerciseProgramBodyScreen> createState() =>
      _ExerciseProgramBodyScreenState();
}

class _ExerciseProgramBodyScreenState extends State<ExerciseProgramBodyScreen> {
  List<ExerciseProgram> exercises = List.empty();
  @override
  void initState() {
    super.initState();
    exercises = widget.exerciseList;
  }

  @override
  Widget build(BuildContext context) {
    double height = MediaQuery.of(context).size.height;
    double width = MediaQuery.of(context).size.width;
    return SafeArea(
        child: Scaffold(
            appBar: AppBar(
              centerTitle: true,
              title: const Text(
                "Training Program",
                style: TextStyle(fontSize: 20),
              ),
            ),
            body: Center(
              child: ListView.builder(
                  itemCount: exercises.length,
                  itemBuilder: ((context, index) => Padding(
                        padding: const EdgeInsets.all(12.0),
                        child: Card(
                            child: Column(
                          children: [
                            ListTile(
                                leading: Container(
                                  width: 40, // İstediğiniz genişliği ayarlayın
                                  height:
                                      40, // İstediğiniz yüksekliği ayarlayın
                                  decoration: BoxDecoration(
                                    shape: BoxShape.circle,
                                    border: Border.all(color: Colors.white),
                                  ),
                                  child: CircleAvatar(
                                      child: Text(
                                          exercises[index].Rating.toString())),
                                ),
                                title: Text(exercises[index].Title.toString()),
                                subtitle: Text(
                                    'Region: ${exercises[index].BodyPart}')),
                            Padding(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 12, vertical: 12),
                              child: ExpandableText(
                                exercises[index].Desc.toString(),
                                expandText: 'show more',
                                maxLines: 2,
                                collapseText: 'show less',
                              ),
                            ),
                          ],
                        )),
                      ))),
            )));
  }
}
