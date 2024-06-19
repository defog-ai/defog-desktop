import pandas as pd

from agents.planner_executor.tool_helpers.tool_param_types import (
    DBColumn,
    DropdownSingleSelect,
    ListWithDefault,
)

async def t_test(
    full_data: pd.DataFrame,
    group_column: DBColumn,
    score_column: DBColumn,
    name_column: DBColumn,
    t_test_type: DropdownSingleSelect = ListWithDefault(
        ["unpaired", "paired"], default_value="unpaired"
    ),
    global_dict: dict = {},
    **kwargs,
):
    """
    This function gets two samples and runs a t-test to check if there is a significant difference between their means.
    There are two ways to run the test: paired and unpaired.
    """
    import pandas as pd
    from scipy import stats
    
    print(group_column)
    print(score_column)
    reactive_vars = {}

    if name_column == "" or name_column is None:
        subset_columns = [group_column, score_column]
    else:
        subset_columns = [group_column, score_column, name_column]

    df = full_data.dropna(subset=subset_columns)
    # TODO add error handling for when there are not enough rows
    # get the two samples
    # next, ensure that the cumulative number of groups for the group_columns is 2

    groups = df[group_column].unique().tolist()
    print(groups)

    # if there are more than 2 groups, we can't run t tests, so return an error
    if len(groups) > 2:
        return {
            "error_message": "More than 2 groups. Consider running a Wilcoxon test."
        }

    # run an unpaired t-test
    if t_test_type == "unpaired":
        # now find all the groups and values
        samples = []
        for group_name in groups:
            sample = df[df[group_column] == group_name]
            sample.name = group_name
            samples.append(sample)

        sample1 = samples[0]
        sample2 = samples[1]

        # now we have all the samples, we can run the t test
        sample_1_values = sample1[score_column]
        sample_2_values = sample2[score_column]

        statistic, p_value = stats.ttest_ind(sample_1_values, sample_2_values)

        analysis = f"t-test between:\nSample 1: {sample1.name}\nSample 2: {sample2.name}\nstatistic: {statistic:.4f}\np-value: {p_value:.4f}"
        if p_value < 0.05:
            significance = "a"
            direction = "positive " if statistic > 0 else "negative "
        else:
            significance = "no"
            direction = ""
        analysis += f"\nThere is {significance} significant {direction}difference between the means of {sample1.name} and {sample2.name}."
        # save statistic and p_value into a dataframe
        reactive_vars = {
            "unpaired t-test": {
                "statistic": statistic,
                "p_value": p_value,
            }
        }
        t_test_df = pd.DataFrame(
            {
                "test_type": ["unpaired t-test"],
                "statistic": [statistic],
                "p_value": [p_value],
            }
        )
    else:
        # run a paired t-test
        sample_1 = df[df[group_column] == groups[0]][score_column]
        sample_1.name = groups[0]
        sample_2 = df[df[group_column] == groups[1]][score_column]
        sample_2.name = groups[1]

        sample_1 = sample_1.set_index(name_column)
        sample_2 = sample_2.set_index(name_column)

        # combine the two samples into one dataframe, with name_col as the index and score_columns as the column
        combined_df = sample_1.join(sample_2, lsuffix="_1", rsuffix="_2")
        combined_df = combined_df.dropna()

        # use scipy.stats.ttest_rel for paired t-test
        statistic, p_value = stats.ttest_rel(
            combined_df[combined_df.columns[0]], combined_df[combined_df.columns[1]]
        )

        analysis = f"Paired t-test between:\nSample 1: {sample_1.name}\nSample 2: {sample_2.name}\nstatistic: {statistic:.4f}\np-value: {p_value:.4f}"
        if p_value < 0.05:
            significance = "a"
            direction = "positive " if statistic > 0 else "negative "
        else:
            significance = "no"
            direction = ""
        analysis += f"\nThere is {significance} significant {direction}difference between the means of {sample_1.name} and {sample_2.name}."
        # save statistic and p_value into a dataframe
        reactive_vars = {
            "paired t-test": {
                "statistic": statistic,
                "p_value": p_value,
            }
        }
        t_test_df = pd.DataFrame(
            {
                "test_type": ["paired t-test"],
                "statistic": [statistic],
                "p_value": [p_value],
            }
        )

    t_test_df.reactive_vars = reactive_vars
    return {
        "outputs": [
            {
                "data": t_test_df,
                "reactive_vars": reactive_vars,
                "analysis": analysis,
            }
        ],
    }


async def wilcoxon_test(
    full_data: pd.DataFrame,
    group_column: DBColumn,
    score_column: DBColumn,
    name_column: DBColumn,
    global_dict: dict = {},
    **kwargs,
):
    """
    This function gets two samples and runs a wilcoxon test to check if there is a significant difference between their means.
    """
    import pandas as pd
    from scipy import stats

    df = full_data.dropna()
    group_name_1, group_name_2 = df[group_column].unique().tolist()

    sample_1 = df[df[group_column] == group_name_1][score_column]
    sample_1.name = group_name_1
    sample_2 = df[df[group_column] == group_name_2][score_column]
    sample_2.name = group_name_2

    sample_1 = sample_1.set_index(name_column)
    sample_2 = sample_2.set_index(name_column)

    # combine the two samples into one dataframe, with name_col as the index and score_columns as the column
    combined_df = sample_1.join(sample_2, lsuffix="_1", rsuffix="_2")
    combined_df = combined_df.dropna()

    # run a wilcoxon test
    statistic, p_value, z_statistic = stats.wilcoxon(
        combined_df[combined_df.columns[0]], sample_2[combined_df.columns[1]]
    )
    analysis = f"Wilcoxon test between:\nSample 1: {sample_1.name}\nSample 2: {sample_2.name}\nstatistic: {statistic:.4f}\np-value: {p_value:.4f}\nz-statistic: {z_statistic:.4f}"
    if p_value < 0.05:
        significance = "a"
        direction = "positive " if statistic > 0 else "negative "
    else:
        significance = "no"
        direction = ""
    analysis += f"\nThere is {significance} significant {direction}difference between the means of {sample_1.name} and {sample_2.name}."
    # save statistic and p_value into a dataframe
    reactive_vars = {
        "wilcoxon test": {
            "statistic": statistic,
            "p_value": p_value,
            "z_statistic": z_statistic,
        }
    }
    wilcoxon_df = pd.DataFrame(
        {
            "test_type": ["wilcoxon test"],
            "statistic": [statistic],
            "p_value": [p_value],
            "z_statistic": [z_statistic],
        }
    )
    wilcoxon_df.reactive_vars = reactive_vars
    return {
        "outputs": [
            {
                "data": wilcoxon_df,
                "reactive_vars": reactive_vars,
                "analysis": analysis,
            }
        ],
    }