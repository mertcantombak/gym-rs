// ignore_for_file: unused_local_variable

import 'dart:math';

import 'package:flutter/material.dart';
import 'package:gym_rs/api/api.dart';
import 'package:gym_rs/models/exerciseProgram.dart';
import 'package:gym_rs/screens/exerciseProgramBody.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'GYMRS',
      theme: ThemeData.dark(),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int enteredBoy = -1, enteredKilo = -1;
  bool _isLoading = false;
  double vki = -1;
  List<int> parametreler = List.empty();
  bool validateBoyKilo = false;
  List<ExerciseProgram> exercises = List.empty();
  String selectedLevel = 'Beginner',
      selectedEq = 'Basic eqs',
      selectedGender = "Male",
      selectedGoal = "Strength",
      selectedTime = "Between 45 and 90";
  int selectedLevelNum = 1,
      selectedEqNum = 2,
      selectedGenderNum = 1,
      selectedGoalNum = 1,
      selectedTimeNum = 2,
      selectedVkiNum = 1;

  final List<String> levels = [
    'Beginner',
    'Intermediate',
    'Expert',
  ];
  final Map<String, int> levelValues = {
    'Beginner': 1,
    'Intermediate': 2,
    'Expert': 3,
  };

  final List<String> eqs = [
    'No-eqs',
    'Basic eqs',
    'Advanced eqs',
  ];
  final Map<String, int> eqValues = {
    'No-eqs': 1,
    'Basic eqs': 2,
    'Advanced eqs': 3,
  };

  final List<String> genders = [
    'Male',
    'Female',
  ];
  final Map<String, int> genderValues = {
    'Male': 1,
    'Female': 2,
  };

  final List<String> goals = [
    'Strength',
    'Plyometrics',
    'Cardio',
    'Stretching',
    'Powerlifting',
  ];

  final Map<String, int> goalValues = {
    'Strength': 1,
    'Plyometrics': 2,
    'Cardio': 3,
    'Stretching': 4,
    'Powerlifting': 5,
  };

  final List<String> times = [
    "Less than 45",
    'Between 45 and 90',
    'More than 90',
  ];
  final Map<String, int> timeValues = {
    "Less than 45": 1,
    'Between 45 and 90': 2,
    'More than 90': 3,
  };
  final boyController = TextEditingController();
  final kiloController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    double height = MediaQuery.of(context).size.height;
    double width = MediaQuery.of(context).size.width;
    return GestureDetector(
      onTap: () => FocusManager.instance.primaryFocus?.unfocus(),
      child: SafeArea(
        child: Scaffold(
          appBar: AppBar(
            centerTitle: true,
            title: const Text(
              "GYMRS",
              style: TextStyle(fontSize: 20),
            ),
          ),
          body: SingleChildScrollView(
            child: Center(
              child: Column(
                children: [
                  const SizedBox(
                    height: 20,
                  ),
                  Row(
                    children: [
                      Expanded(
                        child: Padding(
                          padding: const EdgeInsets.only(right: 8, left: 12),
                          child: TextField(
                            cursorColor: Colors.white,
                            keyboardType: TextInputType.number,
                            onChanged: (value) {
                              setState(() {
                                enteredBoy = int.tryParse(value) ?? 0;
                              });
                            },
                            decoration: const InputDecoration(
                                border: OutlineInputBorder(
                                  borderSide: BorderSide(color: Colors.white),
                                ),
                                enabledBorder: OutlineInputBorder(
                                  borderSide: BorderSide(color: Colors.white),
                                ),
                                focusedBorder: OutlineInputBorder(
                                  borderSide: BorderSide(color: Colors.white),
                                ),
                                labelText: 'Height(cm) ',
                                labelStyle: TextStyle(
                                    color: Colors.white, fontSize: 12)),
                          ),
                        ),
                      ),
                      Expanded(
                        child: Padding(
                          padding: const EdgeInsets.only(right: 12, left: 8),
                          child: TextField(
                            cursorColor: Colors.white,
                            keyboardType: TextInputType.number,
                            onChanged: (value) {
                              setState(() {
                                enteredKilo = int.tryParse(value) ?? 0;
                              });
                            },
                            decoration: const InputDecoration(
                                border: OutlineInputBorder(
                                  borderSide: BorderSide(color: Colors.white),
                                ),
                                enabledBorder: OutlineInputBorder(
                                  borderSide: BorderSide(color: Colors.white),
                                ),
                                focusedBorder: OutlineInputBorder(
                                  borderSide: BorderSide(color: Colors.white),
                                ),
                                labelText: 'Weight(kg)',
                                labelStyle: TextStyle(
                                    color: Colors.white, fontSize: 12)),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(
                    height: 8,
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 5),
                    child: ListTile(
                      isThreeLine: true,
                      trailing: const Text(""),
                      leading: Image.asset('assets/seviye1.png'),
                      title: const Text(
                        'Level',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: DropdownButton<int>(
                        value: levelValues[selectedLevel],
                        items: levels.map((String option) {
                          return DropdownMenuItem<int>(
                            value: levelValues[option],
                            child: Text(
                              option,
                              style: const TextStyle(fontSize: 16),
                            ),
                          );
                        }).toList(),
                        onChanged: (int? value) {
                          setState(() {
                            selectedLevel = levels[(value! - 1)];
                            selectedLevelNum = value;
                          });
                        },
                      ),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 5),
                    child: ListTile(
                      isThreeLine: true,
                      leading: Image.asset('assets/ekipman2.png'),
                      trailing: const Text(""),
                      title: const Text(
                        "Equipment",
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: DropdownButton<int>(
                        value: eqValues[selectedEq],
                        items: eqs.map((String option) {
                          return DropdownMenuItem<int>(
                            value: eqValues[option],
                            child: Text(
                              option,
                              style: const TextStyle(fontSize: 16),
                            ),
                          );
                        }).toList(),
                        onChanged: (int? value) {
                          setState(() {
                            selectedEq = eqs[(value! - 1)];
                            selectedEqNum = value;
                          });
                        },
                      ),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 5),
                    child: ListTile(
                      isThreeLine: true,
                      trailing: const Text(""),
                      leading: Image.asset('assets/cinsiyet.png'),
                      title: const Text(
                        "Gender",
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: DropdownButton<int>(
                        value: genderValues[selectedGender],
                        items: genders.map((String option) {
                          return DropdownMenuItem<int>(
                            value: genderValues[option],
                            child: Text(option),
                          );
                        }).toList(),
                        onChanged: (int? value) {
                          setState(() {
                            selectedGender = genders[(value! - 1)];
                            selectedGenderNum = value;
                          });
                        },
                      ),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 5),
                    child: ListTile(
                      isThreeLine: true,
                      trailing: const Text(""),
                      leading: Image.asset('assets/hedef.png'),
                      title: const Text(
                        "Goal",
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: DropdownButton<int>(
                        value: goalValues[selectedGoal],
                        items: goals.map((String option) {
                          return DropdownMenuItem<int>(
                            value: goalValues[option],
                            child: Text(option),
                          );
                        }).toList(),
                        onChanged: (int? value) {
                          setState(() {
                            selectedGoal = goals[(value! - 1)];
                            selectedGoalNum = value;
                          });
                        },
                      ),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 5),
                    child: ListTile(
                      isThreeLine: true,
                      leading: Image.asset('assets/saat.png'),
                      trailing: const Text(""),
                      title: const Text(
                        "Time",
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: DropdownButton<int>(
                        value: timeValues[selectedTime],
                        items: times.map((String option) {
                          return DropdownMenuItem<int>(
                            value: timeValues[option],
                            child: Text(option),
                          );
                        }).toList(),
                        onChanged: (int? value) {
                          setState(() {
                            selectedTime = times[(value! - 1)];
                            selectedTimeNum = value;
                          });
                        },
                      ),
                    ),
                  ),
                  const SizedBox(
                    height: 20,
                  ),
                  OutlinedButton(
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: Colors.white),
                    ),
                    onPressed: () {
                      _validateBoyKiloFunc();
                      if (!validateBoyKilo) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text(
                              "Enter valid height and weight.",
                              style: TextStyle(color: Colors.white),
                            ),
                            backgroundColor: Colors.red,
                          ),
                        );
                      } else {}
                    },
                    child: const Text(
                      'Get Exercise Program',
                      style: TextStyle(color: Colors.white),
                    ),
                  )
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  _validateBoyKiloFunc() {
    if (enteredBoy > 0 && enteredKilo > 0) {
      validateBoyKilo = true;
      vki = (enteredKilo * 10000) / pow(enteredBoy, 2);
      if (vki < 19) {
        selectedVkiNum = 1;
      } else if (vki < 25) {
        selectedVkiNum = 2;
      } else if (vki < 30) {
        selectedVkiNum = 3;
      } else {
        selectedVkiNum = 4;
      }
      parametreler = [
        selectedLevelNum,
        selectedEqNum,
        selectedGenderNum,
        selectedGoalNum,
        selectedVkiNum,
        selectedTimeNum
      ];
      _postData();
    } else {
      validateBoyKilo = false;
    }
    //print("parametreler: $parametreler");
  }

  _postData() async {
    await Api.PostData(parametreler).then((response) {
      exercises = response;
      if (exercises.isNotEmpty) {
        Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => ExerciseProgramBodyScreen(
                    exerciseList: exercises,
                  )),
        ).then((value) {
          Navigator.pushAndRemoveUntil(
              context,
              MaterialPageRoute(builder: (context) => const MyHomePage()),
              (route) => false);
        });
      } else {}
    });
  }
}
