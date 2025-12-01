package com.example.assignment1;   // <-- change to your actual package if different

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.widget.EditText;
import android.widget.TextView;

public class ExampleUnitTest extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        setupGrading(R.id.score1030, R.id.grade1030);
        setupGrading(R.id.score3040, R.id.grade3040);
        setupGrading(R.id.score3060, R.id.grade3060);
        setupGrading(R.id.score3080, R.id.grade3080);
        setupGrading(R.id.score4050, R.id.grade4050);
    }

    private void setupGrading(int scoreId, int gradeId) {
        EditText scoreInput = findViewById(scoreId);
        TextView gradeOutput = findViewById(gradeId);

        scoreInput.addTextChangedListener(new TextWatcher() {
            @Override public void beforeTextChanged(CharSequence s, int start, int count, int after) {}

            @Override public void onTextChanged(CharSequence s, int start, int before, int count) {
                String text = s.toString().trim();
                if (text.isEmpty()) {
                    gradeOutput.setText("");
                    return;
                }

                Integer score = null;
                try {
                    score = Integer.parseInt(text);
                } catch (NumberFormatException e) {
                    gradeOutput.setText("Invalid");
                    return;
                }

                gradeOutput.setText(getGrade(score));
            }

            @Override public void afterTextChanged(Editable s) {}
        });
    }

    private String getGrade(int score) {
        if (score < 0 || score > 100) return "Invalid";
        if (score <= 39) return "F";
        if (score <= 49) return "D";
        if (score <= 59) return "C";
        if (score <= 69) return "B";
        return "A";
    }
}
