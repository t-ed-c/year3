#include <iostream>
#include <algorithm> // for std::min and std::max, although not used in the final minmax function
using namespace std;

// Function to find minimum and maximum using divide and conquer
void minmax(int* a, int low, int high, int& min, int& max) {
    // If only one element
    if (low == high) {
        max = min = a[low];
    }
    // If two elements
    else if (low == high - 1) {
        if (a[low] < a[high]) {
            min = a[low];
            max = a[high];
        } else {
            min = a[high];
            max = a[low];
        }
    }
    // If more than two elements
    else {
        int mid = (low + high) / 2;
        int min1, max1;

        // Recurse on the first half
        minmax(a, low, mid, min, max);

        // Recurse on the second half
        minmax(a, mid + 1, high, min1, max1);

        // Compare results of both halves to find the overall min and max
        if (max < max1) {
            max = max1;
        }

        if (min > min1) {
            min = min1;
        }
    }
}

int main() {
    int a[10], min, max;
    cout << "Enter 10 elements of the array:\n";
    for (int i = 0; i < 10; i++) {
        cin >> a[i];
    }

    // Call minmax on the full array
    minmax(a, 0, 9, min, max);

    // Output the result
    cout << "Maximum element: " << max << endl;
    cout << "Minimum element: " << min << endl;

    return 0;
}